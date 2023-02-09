from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_staff', 'phone_number', 'last_login', 'date_joined')
    search_fields = ('email', 'username', 'is_staff', 'phone_number')
    readonly_fields = ('id', 'date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ('is_staff', 'is_verified', 'is_active', 'groups')
    fieldsets = ()

    
admin.site.register(User, AccountAdmin)