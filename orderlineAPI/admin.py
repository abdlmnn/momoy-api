from django.contrib import admin
from .models import Orderline

@admin.register(Orderline)
class OrderlineAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'inventory', 'quantity', 'price')
    search_fields = ('order__id', 'inventory__product__name')
