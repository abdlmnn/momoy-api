from rest_framework import serializers
from .models import Orderline
from inventoryAPI.serializers import InventorySerializer

class OrderlineSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer(read_only=True)

    class Meta:
        model = Orderline
        fields = ['id', 'inventory', 'quantity', 'price']
    
    def get_image(self, obj):
        if obj.inventory.image:
            return f"https://momoy-api.onrender.com{obj.inventory.image.url}"
        return None