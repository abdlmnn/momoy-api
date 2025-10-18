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
            # Check if using Cloudinary (production)
            if hasattr(obj.image, 'url') and 'cloudinary' in str(obj.image.url):
                return obj.image.url
            # Local development
            elif hasattr(obj.image, 'url'):
                return f"https://momoy-api.onrender.com{obj.image.url}"
            # Fallback for Cloudinary public_id format
            else:
                return f"https://res.cloudinary.com/dlk1dzj2o/image/upload/{obj.image}"
        return None