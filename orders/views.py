# orders/views.py
from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer
from .models import Order, OrderItem
from accounts.models import Address
from cart.models import Cart
from .serializers import OrderSerializer

class CheckoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer # Sirf response ke liye

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
            if not cart.items.exists():
                return Response({"error": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

            # Assume user ne address ID bheja hai (ab ke liye hardcode karte hain)
            delivery_address = Address.objects.filter(user=user).first()
            if not delivery_address:
                return Response({"error": "Please add a delivery address first."}, status=status.HTTP_400_BAD_REQUEST)

        except Cart.DoesNotExist:
            return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

        # --- Database Transaction Shuru ---
        with transaction.atomic():
            # 1. Total amount calculate karo
            total_amount = sum(
                item.inventory_item.price * item.quantity for item in cart.items.all()
            )

            # 2. Naya Order banao
            order = Order.objects.create(
                user=user,
                delivery_address=delivery_address,
                total_amount=total_amount,
                # Assume order ek hi store se hai
                store=cart.items.first().inventory_item.store
            )

            # 3. Cart items ko Order items mein daalo aur stock kam karo
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product_name=cart_item.inventory_item.product.name,
                    price_at_order=cart_item.inventory_item.price,
                    quantity=cart_item.quantity
                )
                # Sabse zaroori: Stock update karo 
                inventory = cart_item.inventory_item
                inventory.stock_quantity -= cart_item.quantity
                inventory.save()

            # 4. Cart khaali kardo
            cart.items.all().delete()
        # --- Transaction Khatam ---

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Yeh sirf logged-in user ke orders hi return karega
        user = self.request.user
        return Order.objects.filter(user=user).order_by('-created_at')