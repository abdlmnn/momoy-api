from django.contrib import admin
from .models import Chat

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'is_from_user', 'created_at')
    list_filter = ('is_from_user', 'created_at')
    search_fields = ('user__email', 'message')
    ordering = ('-created_at',)
