from rest_framework import serializers
from .models import Orderline

class OrderlineSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='inventory.product.name', read_only=True)
    size = serializers.CharField(source='inventory.size', read_only=True)

    class Meta:
        model = Orderline
        fields = ['id', 'inventory', 'product_name', 'size', 'quantity', 'price']