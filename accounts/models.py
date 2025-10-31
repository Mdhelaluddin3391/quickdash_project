# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    # Email ko optional banate hain
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)

    # Ab username zaroori nahi hai login ke liye
    REQUIRED_FIELDS = []

class Address(models.Model):
    # ... (yeh pehle jaisa hi rahega)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    full_address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return f"Address for {self.user.username}"