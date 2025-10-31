# store/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    icon = models.ImageField(upload_to='category_icons/', null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name

class Store(models.Model):
    # These are your "Dark Stores" or warehouses 
    name = models.CharField(max_length=100)
    # TODO: Add location = models.PointField() later when we set up GeoDjango
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name