# cart/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from inventory.models import StoreInventory
from .serializers import CartSerializer, AddCartItemSerializer

class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated] # सिर्फ लॉग-इन यूजर ही अपना कार्ट देख सकता है

    def get_object(self):
        # हर यूजर का अपना एक कार्ट ढूंढो या बनाओ
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


class AddToCartView(generics.GenericAPIView):
    serializer_class = AddCartItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        inventory_item_id = serializer.validated_data['inventory_item_id']
        quantity = serializer.validated_data['quantity']

        try:
            inventory_item = StoreInventory.objects.get(id=inventory_item_id)
        except StoreInventory.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        cart = Cart.objects.get(user=request.user)

        # चेक करो कि आइटम कार्ट में पहले से है या नहीं
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            inventory_item=inventory_item
        )

        # अगर आइटम नया नहीं है, तो quantity बढ़ा दो, वरना सेट कर दो
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()

        return Response({"success": "Item added to cart"}, status=status.HTTP_200_OK)