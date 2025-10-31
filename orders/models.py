# orders/models.py
from django.db import models
from django.conf import settings

# We need to import models from other apps
from accounts.models import Address
from store.models import Store

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('PREPARING', 'Preparing'),
        ('READY_FOR_PICKUP', 'Ready for Pickup'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)
    delivery_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, default='PENDING')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    # Denormalized data - we store it here directly
    product_name = models.CharField(max_length=255)
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product_name} for Order {self.order.id}"

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20) # e.g., 'SUCCESS', 'FAILED'

    def __str__(self):
        return f"Payment for Order {self.order.id}"