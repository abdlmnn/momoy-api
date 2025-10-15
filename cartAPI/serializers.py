from rest_framework import serializers
from .models import Cart, CartLine

class CartLineSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='inventory.product.name', read_only=True)
    size = serializers.CharField(source='inventory.size', read_only=True)
    price = serializers.DecimalField(source='inventory.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartLine
        fields = ['id', 'inventory', 'product_name', 'size', 'price', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    lines = CartLineSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'user_email', 'is_active', 'lines']