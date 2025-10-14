from rest_framework import serializers
from .models import Product
from inventoryAPI.serializers import InventorySerializer

class ProductSerializer(serializers.ModelSerializer):
    categoryId = serializers.CharField(source='category.id', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    variants = InventorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'categoryId', 'category_name', 'product_type', 'brand', 'created_at', 'variants',]