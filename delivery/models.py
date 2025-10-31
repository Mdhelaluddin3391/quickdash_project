# delivery/models.py
from django.db import models
from django.conf import settings
from orders.models import Order

class RiderProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # TODO: Add current_location = models.PointField() later with GeoDjango
    is_online = models.BooleanField(default=False)
    vehicle_details = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Rider: {self.user.username}"

class Delivery(models.Model):
    STATUS_CHOICES = [
        ('ASSIGNED', 'Assigned'),
        ('PICKED_UP', 'Picked Up'),
        ('DELIVERED', 'Delivered'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    rider = models.ForeignKey(RiderProfile, on_delete=models.SET_NULL, null=True, blank=True)
    pickup_time = models.DateTimeField(null=True, blank=True)
    delivery_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ASSIGNED')

    def __str__(self):
        return f"Delivery for Order {self.order.id}"