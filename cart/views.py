# cart/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from inventory.models import StoreInventory
from .serializers import CartSerializer, AddCartItemSerializer
from django.shortcuts import get_object_or_404 # Naya import
from .serializers import CartSerializer, AddCartItemSerializer, UpdateCartItemSerializer # <-- Naya serializer import kiya

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


class UpdateCartItemView(generics.GenericAPIView):
    # Yeh view CartItem ke 'id' (pk) par kaam karega
    serializer_class = UpdateCartItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        cart_item_id = self.kwargs.get('pk')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_quantity = serializer.validated_data['quantity']
        user_cart = Cart.objects.get(user=request.user)
        
        # Pehle cart item ko check karo ki woh user ke cart mein hai ya nahi
        cart_item = get_object_or_404(
            CartItem, 
            id=cart_item_id, 
            cart=user_cart
        )

        if new_quantity > 0:
            # Agar quantity 0 se zyada hai, toh update karo
            cart_item.quantity = new_quantity
            cart_item.save()
            return Response({"success": "Cart item quantity updated."}, status=status.HTTP_200_OK)
        else:
            # Agar quantity 0 ya usse kam hai, toh item ko hata do (Remove)
            cart_item.delete()
            return Response({"success": "Item removed from cart."}, status=status.HTTP_204_NO_CONTENT)

# Agar hume sirf delete karna ho toh uske liye DeleteAPIView use kar sakte hain:
class RemoveCartItemView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Yeh queryset ensure karega ki user sirf apne cart items ko delete kar sakta hai
        user_cart = get_object_or_404(Cart, user=self.request.user)
        return CartItem.objects.filter(cart=user_cart)