from django.contrib import admin
from .models import Inventory

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'size', 'price', 'stock', 'is_new','is_available', 'image_url')
    list_filter = ('is_available', 'is_new')
    search_fields = ('product__name', 'size')
    # readonly_fields = ('display_image',)
