# orders/urls.py
from django.urls import path
# OrderHistoryView ko import karo
from .views import CheckoutView, OrderHistoryView

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    # Yeh naya URL hai
    path('', OrderHistoryView.as_view(), name='order-history'),
]