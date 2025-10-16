from rest_framework import serializers
from .models import Order
from orderlineAPI.serializers import OrderlineSerializer
from paymentAPI.serializers import PaymentSerializer

class OrderSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    orderlines = serializers.SerializerMethodField()
    payment = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'user_email', 'total_amount', 'status', 'created_at', 'updated_at', 'orderlines', 'payment']

    def get_orderlines(self, obj):
        orderlines = obj.orderlines.all()
        return OrderlineSerializer(orderlines, many=True, context=self.context).data

    def get_payment(self, obj):
        if hasattr(obj, 'payment'):
            return PaymentSerializer(obj.payment, context=self.context).data
        return None