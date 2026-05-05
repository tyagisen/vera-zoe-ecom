from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from apps.orders.models import Address, Order, OrderItem
from apps.orders.api.serializers import (
    AddressSerializer,
    CreateOrderSerializer,
    OrderSerailizer,
)
from apps.orders.services import create_order_from_cart


class AddressListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user = self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)