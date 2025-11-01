# orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product_name', 'price_at_order', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'store',
            'delivery_address',
            'total_amount',
            'status',
            'payment_status',
            'created_at',
            'items'
        ]

class OrderStatusUpdateSerializer(serializers.Serializer):
    # Sirf woh status allow karo jo store staff use karega
    STATUS_CHOICES = ['PREPARING', 'READY_FOR_PICKUP', 'CANCELLED']
    
    status = serializers.ChoiceField(choices=STATUS_CHOICES)