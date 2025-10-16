from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Order
from .serializers import OrderSerializer
from cartAPI.models import Cart, CartLine
from orderlineAPI.models import Orderline
from django.db import transaction

class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        with transaction.atomic():
            # Get user's active cart
            cart = Cart.objects.filter(user=request.user, is_active=True).first()
            if not cart or not cart.lines.exists():
                return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

            # Calculate total
            total_amount = sum(line.inventory.price * line.quantity for line in cart.lines.all())

            # Create order
            order = Order.objects.create(user=request.user, total_amount=total_amount)

            # Move cart lines → order lines
            for line in cart.lines.all():
                Orderline.objects.create(
                    order=order,
                    inventory=line.inventory,
                    quantity=line.quantity,
                    price=line.inventory.price
                )

                # Update inventory stock
                line.inventory.stock -= line.quantity
                if line.inventory.stock < 0:
                    transaction.set_rollback(True)
                    return Response({"error": f"Insufficient stock for {line.inventory.product.name}"}, status=status.HTTP_400_BAD_REQUEST)
                line.inventory.save()

            # Clear cart
            cart.lines.all().delete()
            cart.is_active = False
            cart.save()

            serializer = OrderSerializer(order)
            return Response({
                "message": "Order placed successfully",
                "order": serializer.data
            }, status=status.HTTP_201_CREATED)

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
