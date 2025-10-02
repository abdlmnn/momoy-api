from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source='order.id', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'order', 'order_id', 'amount', 'method', 'status', 'transaction_id', 'proof_image', 'created_at']