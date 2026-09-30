from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

# Register your models here.

@admin.register(CustomUser) # Register custom user model
class UserAdmin(BaseUserAdmin):
    # Define fields/columns
    list_display = ("username", "email", "phone_number", 
                    "first_name", "last_name", "role", "is_staff",)
    
    # Filter widget
    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    
    # Adds phone number and role when editing view in admin
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Platform Profile Details", {"fields": ("role", "phone_number")}),
    )
    
    # Adds phone number and role when creating view in admin
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Platform Profile Details", {"fields": ("role", "phone_number")}),
    )
