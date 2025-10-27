from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings
import uuid

class UserAddress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
    )
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  
    longitude = models.DecimalField(max_digits=9, decimal_places=6) 
    is_default = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'address')

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True, unique=True)

    def __str__(self):
        return self.email or self.username

class PendingEmailVerification(models.Model):
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email

class PendingLoginLink(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class LoginVerification(models.Model):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    # Profile can include additional fields if needed in the future
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.user.email}"