from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source='order.id', read_only=True)
    order_total = serializers.DecimalField(source='order.total_amount', max_digits=10, decimal_places=2, read_only=True)


    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'order_id', 'amount', 'method', 
            'status', 'proof_image', 'created_at', 'order_total'
        ]
    
    def validate(self, data):
        method = data.get('method')
        proof_image = data.get('proof_image')

        if method == 'gcash' and not proof_image:
            raise serializers.ValidationError({
                "proof_image": "Proof of payment is required for GCash payments."
            })
        elif method == 'cod' and proof_image:
            raise serializers.ValidationError({
                "proof_image": "Proof image should not be uploaded for Cash on Delivery."
            })
        return data

    def create(self, validated_data):
        payment = super().create(validated_data)
        if payment.method == 'cod':
            payment.status = 'delivery' 
            payment.save()
        return payment