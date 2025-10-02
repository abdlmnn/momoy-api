from django.contrib import admin
from .models import Inventory

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'size', 'price', 'stock', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('product__name', 'size')
