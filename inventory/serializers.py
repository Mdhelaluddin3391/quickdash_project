# inventory/serializers.py
from rest_framework import serializers
from .models import StoreInventory

class StoreInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreInventory
        # हम सिर्फ कीमत और स्टॉक दिखाना चाहते हैं
        fields = ['price', 'stock_quantity']