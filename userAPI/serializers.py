from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserAddress, UserProfile

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

class UserProfileSerializer(serializers.ModelSerializer):
    # Include user fields for updating
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    phone = serializers.CharField(source='user.phone', required=False, allow_blank=True)
    is_superuser = serializers.BooleanField(source='user.is_superuser', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'is_superuser', 'created_at', 'updated_at']
        read_only_fields = ['id', 'is_superuser', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        # Handle user fields update
        user_data = validated_data.pop('user', {})
        user = instance.user

        for attr, value in user_data.items():
            if attr == 'email':
                # Check if email is already taken by another user
                if User.objects.filter(email=value).exclude(id=user.id).exists():
                    raise serializers.ValidationError({"email": "Email already in use"})
            setattr(user, attr, value)
        user.save()

        # Update profile instance
        return super().update(instance, validated_data)