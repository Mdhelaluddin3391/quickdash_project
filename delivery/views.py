# delivery/views.py

from django.db import transaction
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import RiderProfile, Delivery
from .serializers import RiderProfileSerializer, RiderOrderSerializer # <- Correction
from orders.models import Order


class RiderProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = RiderProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return RiderProfile.objects.get(user=self.request.user)
        except RiderProfile.DoesNotExist:
            # Yeh line error rokegi agar user rider na ho
            return None


class AvailableOrdersView(generics.ListAPIView):
    serializer_class = RiderOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            status='READY_FOR_PICKUP',
            delivery__rider__isnull=True
        ).order_by('-created_at')


class AcceptOrderView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs.get('pk')
        
        # Rider profile ko safely get karo
        try:
            rider_profile = request.user.riderprofile
        except RiderProfile.DoesNotExist:
            return Response({"error": "You are not a rider."}, status=status.HTTP_403_FORBIDDEN)

        try:
            order = Order.objects.get(id=order_id, status='READY_FOR_PICKUP')
        except Order.DoesNotExist:
            return Response({"error": "Order is not available for pickup."}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            delivery, created = Delivery.objects.get_or_create(order=order)
            if not created and delivery.rider:
                 return Response({"error": "Order has already been taken."}, status=status.HTTP_400_BAD_REQUEST)

            delivery.rider = rider_profile
            delivery.save()
            order.status = 'OUT_FOR_DELIVERY'
            order.save()

        return Response({"success": f"Order {order.id} accepted."}, status=status.HTTP_200_OK)


class MarkDeliveredView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs.get('pk')
        try:
            rider_profile = request.user.riderprofile
        except RiderProfile.DoesNotExist:
            return Response({"error": "You are not a rider."}, status=status.HTTP_403_FORBIDDEN)

        try:
            delivery = Delivery.objects.get(
                order__id=order_id,
                rider=rider_profile
            )
        except Delivery.DoesNotExist:
            return Response({"error": "Delivery not found or not assigned to you."}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            delivery.status = 'DELIVERED'
            delivery.delivery_time = timezone.now()
            delivery.save()
            order = delivery.order
            order.status = 'DELIVERED'
            order.save()

        return Response({"success": f"Order {order.id} marked as delivered."}, status=status.HTTP_200_OK)