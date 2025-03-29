from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the CustomUser model.
    """
    model = CustomUser
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'address', 'city', 'state', 'country', 'postal_code', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'address', 'city', 'state', 'country', 'postal_code', 'profile_picture')}),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)