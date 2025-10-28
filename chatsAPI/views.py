from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Chat
from .serializers import ChatSerializer

class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chats = Chat.objects.filter(user=request.user).order_by('-created_at')
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        order_id = data.get('order')

        # Validate order if provided
        if order_id:
            try:
                from orderAPI.models import Order
                order = Order.objects.get(id=order_id, user=request.user)
                data['order'] = order.id
            except Order.DoesNotExist:
                return Response({"error": "Order not found or doesn't belong to user"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChatSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
