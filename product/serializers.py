from rest_framework import serializers
from .models import *

class TypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Type
    fields = ['id', 'name']