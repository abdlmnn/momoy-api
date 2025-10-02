from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'is_new', 'created_at')
    list_filter = ('is_new', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)