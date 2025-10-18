from rest_framework import serializers
from .models import Inventory
import os
from cloudinary import utils

class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    image = serializers.SerializerMethodField()
    

    class Meta:
        model = Inventory
        fields = ['id', 'product', 'product_name', 'size', 'price', 'stock', 'image', 'is_new','is_available']

    # def get_image(self, obj):
    #     if obj.inventory.image:
    #         return f"https://momoy-api.onrender.com{obj.inventory.image.url}"
    #     return None

    def get_image(self, obj):
        if obj.image:
            # For Cloudinary public_id format
            return f"https://res.cloudinary.com/dlk1dzj2o/image/upload/{obj.image}.png"
        return None