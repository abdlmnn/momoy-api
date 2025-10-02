from rest_framework import serializers
from .models import Chat

class ChatSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'user', 'user_email', 'message', 'is_from_user', 'created_at']