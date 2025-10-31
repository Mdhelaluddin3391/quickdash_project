# cart/urls.py
from django.urls import path
from .views import CartView, AddToCartView

urlpatterns = [
    path('', CartView.as_view(), name='view-cart'),
    path('add-item/', AddToCartView.as_view(), name='add-to-cart'),
]