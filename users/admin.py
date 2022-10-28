from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['id', 'user_id', 'date_joined', 'is_active']
    list_display_links = ['id', 'user_id']
    ordering = ['date_joined',]
    fieldsets = [
        (None, {'fields': ['user_id', 'password', 'user_name', 'email', 'address',
                           'is_superuser', 'is_staff', 'is_active', 'user_permissions']}),
        ('Date information', {'fields': ['date_joined', 'last_login']})
    ]

admin.site.register(User, CustomUserAdmin)
