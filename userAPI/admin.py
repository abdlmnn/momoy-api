from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'latitude', 'longitude', 'is_default')
    # list_filter = ('is_default')
    search_fields = ('user__email', 'address')

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    ist_display = ('id', 'username', 'email', 'first_name', 'last_name', 'phone', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'phone')
    ordering = ('id',)

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone',)}),
    )

@admin.register(PendingEmailVerification)
class PendingEmailVerificationAdmin(admin.ModelAdmin):
    list_display = ("email", "token", "created_at")
    search_fields = ("email",)
    ordering = ("-created_at",)