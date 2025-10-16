from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import PaymentSerializer

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.filter(order__user=request.user).order_by('-created_at')
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.validated_data['order']
            if order.user != request.user:
                return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer.save(amount=order.total_amount)
            return Response({
                "message": "Payment recorded successfully",
                "payment": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

