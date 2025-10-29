from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from .models import Payment
from .serializers import PaymentSerializer
from orderAPI.models import Order
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db import transaction
import stripe
from django.conf import settings

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

@api_view(['POST'])
def create_payment_intent(request):
    """Create Stripe payment intent for an order"""
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

    order_id = request.data.get('order_id')
    amount = request.data.get('amount')
    currency = request.data.get('currency', 'php')

    if not order_id or not amount:
        return Response({'error': 'order_id and amount are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Validate order belongs to user
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if payment already exists
    if hasattr(order, 'payment'):
        return Response({'error': 'Payment already exists for this order'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Set Stripe API key
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Create payment intent
        intent = stripe.PaymentIntent.create(
            amount=int(float(amount) * 100),  # Convert to cents
            currency=currency,
            metadata={
                'order_id': str(order.id),
                'user_email': request.user.email
            }
        )

        return Response({
            'client_secret': intent.client_secret,
            'payment_intent_id': intent.id,
            'amount': amount,
            'currency': currency
        })

    except stripe.error.StripeError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f'Unexpected error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
