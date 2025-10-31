# delivery/serializers.py
from rest_framework import serializers
from .models import RiderProfile
from orders.models import Order

class RiderProfileSerializer(serializers.ModelSerializer):
    # We also want to show the user's name and phone number
    username = serializers.CharField(source='user.username', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)

    class Meta:
        model = RiderProfile
        fields = ['username', 'phone_number', 'is_online', 'vehicle_details']

class RiderOrderSerializer(serializers.ModelSerializer):
    # Hum customer ka naam aur address bhi dikhana chahte hain
    customer_name = serializers.CharField(source='user.username', read_only=True)
    delivery_address = serializers.CharField(source='delivery_address.full_address', read_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'store_name', 'customer_name', 'delivery_address', 'total_amount', 'status']