from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Orderline
from .serializers import OrderlineSerializer

class OrderlineView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get orderlines for user's orders
        orderlines = Orderline.objects.filter(order__user=request.user).order_by('-order__created_at')
        serializer = OrderlineSerializer(orderlines, many=True)
        return Response(serializer.data)
