# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# We are using the default UserAdmin for our custom User model
admin.site.register(User, UserAdmin)