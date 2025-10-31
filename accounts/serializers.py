# accounts/serializers.py
from rest_framework import serializers

class OTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

class OTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)