from rest_framework import serializers
from .models import Inventory
import os
from cloudinary import utils

class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    image = serializers.SerializerMethodField()
    isNew = serializers.BooleanField(source='is_new', read_only=True)
    

    class Meta:
        model = Inventory
        fields = ['id', 'product', 'product_name', 'size', 'price', 'stock', 'image', 'is_new','is_available']

    def get_image(self, obj):
        return obj.display_image

    # def get_image(self, obj):
    #     if obj.image:
    #         # Cloudinary URLs are already full URLs
    #         return obj.image.url
    #     return None

    # def get_image(self, obj):
    #     if obj.image:
    #         # Cloudinary already returns full URL in production
    #         request = self.context.get('request')
    #         if request and obj.image.url.startswith('/'):
    #             # Build full URL for local files
    #             return request.build_absolute_uri(obj.image.url)
    #         return obj.image.url
    #     return None
    
    # def get_image(self, obj):
    #     if obj.image:
    #         # Use full URL so Expo can access it
    #         request = self.context.get('request')
    #         if request:
    #             return request.build_absolute_uri(obj.image.url)
    #         # fallback: manually prepend domain
    #         return f"https://momoy-api.onrender.com{obj.image.url}"
    #     return None

    # def get_image(self, obj):
    #     if obj.image:
    #         request = self.context.get('request')
    #         if request:
    #             return request.build_absolute_uri(obj.image.url)  # full URL
    #         return obj.image.url  # fallback relative URL
    #     return None

    # def get_image(self, obj):
    #     if obj.image:
    #         return f"https://momoy-api.onrender.com{obj.inventory.image.url}"
    #     return None
    
    # def get_image(self, obj):
    #     if obj.image:
    #         # Always return the full URL from the image field
    #         # Cloudinary will handle production URLs automatically
    #         return obj.image.url
    #     return None