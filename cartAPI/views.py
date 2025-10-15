from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Cart, CartLine
from .serializers import CartSerializer, CartLineSerializer
from inventoryAPI.models import Inventory


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get or create an active cart for the user
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):
        """
        Add an inventory item to the user's active cart.
        If the item already exists, increase its quantity.
        Updates inventory stock & availability.
        """
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        serializer = CartLineSerializer(data=request.data)

        if serializer.is_valid():
            inventory = serializer.validated_data['inventory']
            quantity = serializer.validated_data.get('quantity', 1)

            # Check available stock
            if inventory.stock < quantity:
                return Response(
                    {"error": f"Not enough stock. Available: {inventory.stock}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            existing_line = CartLine.objects.filter(cart=cart, inventory=inventory).first()
            if existing_line:
                additional_qty = quantity
                if inventory.stock < additional_qty:
                    return Response(
                        {"error": f"Not enough stock to add more. Available: {inventory.stock}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                existing_line.quantity += additional_qty
                existing_line.save()

                # Reduce stock
                inventory.stock -= additional_qty
            else:
                # Create new line and reduce stock
                CartLine.objects.create(cart=cart, inventory=inventory, quantity=quantity)
                inventory.stock -= quantity

            # Update availability
            if inventory.stock <= 0:
                inventory.stock = 0
                inventory.is_available = False
            else:
                inventory.is_available = True

            inventory.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def put(self, request, pk):
        """
        Update a specific cart line (e.g., change quantity)
        Adjusts inventory stock & availability accordingly.
        """
        cart_line = get_object_or_404(CartLine, pk=pk, cart__user=request.user, cart__is_active=True)
        old_quantity = cart_line.quantity
        serializer = CartLineSerializer(cart_line, data=request.data, partial=True)

        if serializer.is_valid():
            new_quantity = serializer.validated_data.get('quantity', old_quantity)
            inventory = cart_line.inventory
            difference = new_quantity - old_quantity

            # If increasing quantity
            if difference > 0:
                if inventory.stock < difference:
                    return Response(
                        {"error": f"Not enough stock to increase quantity. Available: {inventory.stock}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                inventory.stock -= difference
            elif difference < 0:
                # Return stock if quantity decreases
                inventory.stock += abs(difference)

            # Update availability
            if inventory.stock <= 0:
                inventory.stock = 0
                inventory.is_available = False
            else:
                inventory.is_available = True

            inventory.save()
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def delete(self, request, pk):
        """
        Remove a specific cart line from the user's cart.
        Returns stock to inventory & updates availability.
        """
        cart_line = get_object_or_404(CartLine, pk=pk, cart__user=request.user, cart__is_active=True)
        inventory = cart_line.inventory

        # Return stock
        inventory.stock += cart_line.quantity

        # Update availability
        if inventory.stock > 0:
            inventory.is_available = True

        inventory.save()
        cart_line.delete()

        return Response({"message": "Removed from cart"}, status=status.HTTP_204_NO_CONTENT)
