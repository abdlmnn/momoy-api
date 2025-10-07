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