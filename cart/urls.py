# cart/urls.py
from django.urls import path
from .views import CartView, AddToCartView

urlpatterns = [
    path('', CartView.as_view(), name='view-cart'),
    path('add-item/', AddToCartView.as_view(), name='add-to-cart'),
    path('update-item/<int:pk>/', UpdateCartItemView.as_view(), name='update-cart-item'),
    path('remove-item/<int:pk>/', RemoveCartItemView.as_view(), name='remove-cart-item'),
]