# cart/models.py
from django.db import models
from django.conf import settings
from inventory.models import StoreInventory

class Cart(models.Model):
    # Using a OneToOneField ensures each user has only one cart
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    # This links to a specific product in a specific store's inventory
    inventory_item = models.ForeignKey(StoreInventory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.inventory_item.product.name} in cart for {self.cart.user.username}"