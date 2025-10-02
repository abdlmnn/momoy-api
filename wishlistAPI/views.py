from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Wishlist
from .serializers import WishlistSerializer

class WishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist_items = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlist_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            # Check if item already in wishlist
            existing = Wishlist.objects.filter(
                user=request.user, 
                product=serializer.validated_data['product']
            ).first()
            if existing:
                return Response({"message": "Product already in wishlist"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WishlistDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        wishlist_item = get_object_or_404(Wishlist, pk=pk, user=request.user)
        wishlist_item.delete()
        return Response({"message": "Removed from wishlist"}, status=status.HTTP_204_NO_CONTENT)
