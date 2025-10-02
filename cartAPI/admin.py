from django.contrib import admin
from .models import Cart

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'inventory', 'quantity', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__email', 'inventory__product__name')
