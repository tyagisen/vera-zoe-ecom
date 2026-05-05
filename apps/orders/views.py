from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from apps.orders.models import Address, Order, OrderItem
from apps.orders.api.serializers import (
    AddressSerializer,
    CreateOrderSerializer,
    OrderSerializer,
)
from apps.orders.services import create_order_from_cart


class AddressListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user = self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderCreateAPIView(generics.GenericAPIView):
    serializer_class = CreateOrderSerializer
    permission_classes = [permissions.IsAuthenticated]


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = create_order_from_cart(
            user=request.user, address_id=serializer.validated_data["address_id"],
        )
        output_serializer =OrderSerializer(order)
        return Response(output_serializer.data,status=status.HTTP_201_CREATED)


class OrderListAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items").select_related("address")
    


class OrderDetailAPIView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items").select_related("address")