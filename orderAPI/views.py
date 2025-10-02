from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Order
from .serializers import OrderSerializer

class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Create order from cart
        from cartAPI.models import Cart
        from orderlineAPI.models import Orderline

        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items:
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        total_amount = sum(item.inventory.price * item.quantity for item in cart_items)

        order = Order.objects.create(user=request.user, total_amount=total_amount)

        for item in cart_items:
            Orderline.objects.create(
                order=order,
                inventory=item.inventory,
                quantity=item.quantity,
                price=item.inventory.price
            )
            # Reduce stock
            item.inventory.stock -= item.quantity
            item.inventory.save()

        cart_items.delete()  # Clear cart

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
