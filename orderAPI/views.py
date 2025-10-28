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
from .serializers import AdminOrderSerializer

class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = (
            Order.objects.filter(user=request.user)
            .select_related('payment')  # <-- ensures payment is included
            .prefetch_related('orderlines__inventory')  # fetch orderlines + inventory
            .order_by('-created_at')
        )
        serializer = OrderSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        try:
            with transaction.atomic():
                cart = Cart.objects.filter(user=request.user, is_active=True).first()
                if not cart or not cart.lines.exists():
                    return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

                total_amount = sum(line.inventory.price * line.quantity for line in cart.lines.all())

                order = Order.objects.create(user=request.user, total_amount=total_amount)

                for line in cart.lines.all():
                    if line.inventory.stock < line.quantity:
                        raise ValueError(f"Insufficient stock for {line.inventory.product.name}")

                    Orderline.objects.create(
                        order=order,
                        inventory=line.inventory,
                        quantity=line.quantity,
                        price=line.inventory.price
                    )

                    line.inventory.stock -= line.quantity
                    line.inventory.save()

                cart.lines.all().delete()
                cart.is_active = False
                cart.save()

            serializer = OrderSerializer(order)
            return Response({
                "message": "Order placed successfully",
                "order": serializer.data
            }, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Unexpected error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(
            Order.objects.select_related('payment').prefetch_related('orderlines__inventory'),
            pk=pk,
            user=request.user
        )
        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data)

class AdminOrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_superuser:
            return Response({"error": "Admin access required"}, status=status.HTTP_403_FORBIDDEN)

        orders = Order.objects.all().select_related('payment').prefetch_related('orderlines__inventory__product').order_by('-created_at')
        serializer = AdminOrderSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)

class AdminOrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        if not request.user.is_superuser:
            return Response({"error": "Admin access required"}, status=status.HTTP_403_FORBIDDEN)

        try:
            order = Order.objects.select_related('payment').prefetch_related('orderlines__inventory__product').get(pk=pk)
            serializer = AdminOrderSerializer(order, context={'request': request})
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        if not request.user.is_superuser:
            return Response({"error": "Admin access required"}, status=status.HTTP_403_FORBIDDEN)

        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        if not new_status:
            return Response({"error": "Status is required"}, status=status.HTTP_400_BAD_REQUEST)

        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response({"error": f"Invalid status. Valid options: {', '.join(valid_statuses)}"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save()

        serializer = AdminOrderSerializer(order, context={'request': request})
        return Response({
            "message": f"Order status updated to {new_status}",
            "order": serializer.data
        })
