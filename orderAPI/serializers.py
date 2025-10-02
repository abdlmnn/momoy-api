from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    orderlines = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'user_email', 'total_amount', 'status', 'created_at', 'updated_at', 'orderlines']

    def get_orderlines(self, obj):
        from orderlineAPI.serializers import OrderlineSerializer
        orderlines = obj.orderlines.all()
        return OrderlineSerializer(orderlines, many=True).data