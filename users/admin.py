from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']

admin.site.register(CustomUser, CustomUserAdmin)


