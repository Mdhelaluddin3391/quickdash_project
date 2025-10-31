# store/serializers.py
from rest_framework import serializers
from .models import Category, Product
# inventory serializer को इम्पोर्ट करें
from inventory.serializers import StoreInventorySerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon']

class ProductSerializer(serializers.ModelSerializer):
    # यह लाइन प्रोडक्ट से जुड़ी सभी इन्वेंट्री को दिखाएगी
    inventory = StoreInventorySerializer(many=True, read_only=True, source='storeinventory_set')

    class Meta:
        model = Product
        # 'inventory' को fields में जोड़ें
        fields = ['id', 'name', 'description', 'category', 'image', 'inventory']