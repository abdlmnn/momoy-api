from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid

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