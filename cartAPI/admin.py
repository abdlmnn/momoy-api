from django.contrib import admin
from .models import *

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'is_active']
    list_filter = ['is_active']


@admin.register(CartLine)
class CartLineAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'inventory', 'quantity']
    list_filter = ['inventory']