# accounts/urls.py
from django.urls import path
from .views import SendOTPView, VerifyOTPView, DeleteAccountView

urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('delete/', DeleteAccountView.as_view(), name='delete-account'),
]