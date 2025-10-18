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
    
    def get_image(self, obj):
        if obj.image:
            # Return full Cloudinary URL since images are stored in Cloudinary
            from cloudinary_storage.storage import MediaCloudinaryStorage
            storage = MediaCloudinaryStorage()
            return storage.url(str(obj.image))
        return None