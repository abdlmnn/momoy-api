from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import PaymentSerializer
from orderAPI.models import Order
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db import transaction

@method_decorator(csrf_exempt, name='dispatch')
class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.filter(order__user=request.user).order_by('-created_at')
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a payment (COD or GCash) for an order"""
        order_id = request.data.get('order')
        method = request.data.get('method')
        proof_image = request.FILES.get('proof_image')
        transaction_id = request.data.get('transaction_id')

        # Validate order
        order = get_object_or_404(Order, id=order_id, user=request.user)

        # Prevent duplicate payment
        if hasattr(order, 'payment'):
            return Response({'error': 'Payment already exists for this order.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create payment record
        with transaction.atomic():
            payment = Payment.objects.create(
                order=order,
                amount=order.total_amount,
                method=method,
                # status='completed' if method == 'gcash' else 'pending',
                status='completed' if method in ['gcash', 'stripe'] else 'pending',
                proof_image=proof_image if method == 'gcash' else None,
                transaction_id=transaction_id if method == 'stripe' else None
            )

            # If COD, immediately mark as confirmed
            if method == 'cod':
                order.status = 'pending'
                order.save()
              

        serializer = PaymentSerializer(payment)
        return Response({
            'message': 'Payment created successfully',
            'payment': serializer.data
        }, status=status.HTTP_201_CREATED)
