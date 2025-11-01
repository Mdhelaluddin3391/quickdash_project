# orders/urls.py
from django.urls import path
# OrderHistoryView ko import karo
from .views import CheckoutView, OrderHistoryView, StoreOrderUpdateView

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    # Yeh naya URL hai
    path('', OrderHistoryView.as_view(), name='order-history'),
    path('<int:pk>/update-status/', StoreOrderUpdateView.as_view(), name='store-update-order-status'),
]