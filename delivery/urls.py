
# delivery/urls.py
from django.urls import path
# Naye view ko import karo
from .views import RiderProfileView, AvailableOrdersView
from .views import RiderProfileView, AvailableOrdersView, AcceptOrderView, MarkDeliveredView

urlpatterns = [
    path('profile/', RiderProfileView.as_view(), name='rider-profile'),
    path('orders/available/', AvailableOrdersView.as_view(), name='available-orders'), # Yeh naya URL hai
    path('orders/<int:pk>/accept/', AcceptOrderView.as_view(), name='accept-order'),
    path('orders/<int:pk>/delivered/', MarkDeliveredView.as_view(), name='mark-delivered'),
]