from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Add custom fields to the admin form
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_image', 'bio')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('profile_image', 'bio')}),
    )
