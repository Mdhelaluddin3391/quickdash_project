# inventory/models.py
from django.db import models
from store.models import Store, Product

class StoreInventory(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)

    class Meta:
        # This ensures that a product can only have one entry per store
        unique_together = ('store', 'product')

    def __str__(self):
        return f'{self.product.name} at {self.store.name}'