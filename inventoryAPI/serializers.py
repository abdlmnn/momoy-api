from rest_framework import serializers
from .models import Inventory

class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    image = serializers.SerializerMethodField()
    

    class Meta:
        model = Inventory
        fields = ['id', 'product', 'product_name', 'size', 'price', 'stock', 'image', 'is_new','is_available']
    
    def get_image(self, obj):
        request = self.context.get('request')  # Optional, if you want absolute URL
        if obj.image:
            # If you have MEDIA_URL exposed
            return f"https://momoy-api.onrender.com{obj.image.url}"
        return None