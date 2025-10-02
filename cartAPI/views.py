from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Cart
from .serializers import CartSerializer

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            # Check if item already in cart
            existing = Cart.objects.filter(user=request.user, inventory=serializer.validated_data['inventory']).first()
            if existing:
                existing.quantity += serializer.validated_data['quantity']
                existing.save()
                serializer = CartSerializer(existing)
                return Response(serializer.data)
            else:
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
        serializer = CartSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
        cart_item.delete()
        return Response({"message": "Removed from cart"}, status=status.HTTP_204_NO_CONTENT)
