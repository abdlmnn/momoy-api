from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserAddress

User = get_user_model()

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['id', 'address', 'latitude', 'longitude', 'is_default']

# class EmailSignupSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)

#     def validate_email(self, value):
#         if User.objects.filter(email=value).exists():
#             raise serializers.ValidationError("User with this email already exists")
#         return value
class EmailSignupSerializer(serializers.Serializer):
    email = serializers.EmailField()