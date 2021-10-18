from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authentication.models import User


@admin.register(User)
class AdminUser(UserAdmin):
    list_display = (
        'email', 'is_active', 'is_staff', 'is_superuser', 'created_at'
    )
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    list_filter = ('email', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
