# cart/serializers.py
from rest_framework import serializers
from .models import Cart, CartItem
from inventory.models import StoreInventory
from store.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    # हम सिर्फ inventory_item का ID नहीं, बल्कि पूरी प्रोडक्ट जानकारी दिखाना चाहते हैं
    # इसके लिए हम product serializer का इस्तेमाल करेंगे
    product = ProductSerializer(source='inventory_item.product', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    # यह cart के अंदर मौजूद सभी items को दिखाएगा
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']


class AddCartItemSerializer(serializers.Serializer):
    inventory_item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class UpdateCartItemSerializer(serializers.Serializer):
    # Quantity update karne ke liye sirf quantity ki zaroorat hai
    quantity = serializers.IntegerField(min_value=0) 
    # Agar quantity 0 aati hai, toh hum use remove kar denge