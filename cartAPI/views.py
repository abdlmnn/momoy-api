from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Cart, CartLine
from .serializers import CartSerializer, CartLineSerializer

# class CartView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         cart_items = Cart.objects.filter(user=request.user)
#         serializer = CartSerializer(cart_items, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CartSerializer(data=request.data)
#         if serializer.is_valid():
#             # Check if item already in cart
#             existing = Cart.objects.filter(user=request.user, inventory=serializer.validated_data['inventory']).first()
#             if existing:
#                 existing.quantity += serializer.validated_data['quantity']
#                 existing.save()
#                 serializer = CartSerializer(existing)
#                 return Response(serializer.data)
#             else:
#                 serializer.save(user=request.user)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CartDetailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def put(self, request, pk):
#         cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
#         serializer = CartSerializer(cart_item, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
#         cart_item.delete()
#         return Response({"message": "Removed from cart"}, status=status.HTTP_204_NO_CONTENT)


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get or create an active cart for the user
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        """
        Add an inventory item to the user's active cart.
        If the item already exists, increase its quantity.
        """
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        serializer = CartLineSerializer(data=request.data)

        if serializer.is_valid():
            inventory = serializer.validated_data['inventory']
            quantity = serializer.validated_data.get('quantity', 1)

            existing_line = CartLine.objects.filter(cart=cart, inventory=inventory).first()
            if existing_line:
                existing_line.quantity += quantity
                existing_line.save()
                return Response(CartLineSerializer(existing_line).data, status=status.HTTP_200_OK)
            else:
                line = CartLine.objects.create(cart=cart, inventory=inventory, quantity=quantity)
                return Response(CartLineSerializer(line).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        """
        Update a specific cart line (e.g., change quantity)
        """
        cart_line = get_object_or_404(CartLine, pk=pk, cart__user=request.user, cart__is_active=True)
        serializer = CartLineSerializer(cart_line, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Remove a specific cart line from the user's cart
        """
        cart_line = get_object_or_404(CartLine, pk=pk, cart__user=request.user, cart__is_active=True)
        cart_line.delete()
        return Response({"message": "Removed from cart"}, status=status.HTTP_204_NO_CONTENT)