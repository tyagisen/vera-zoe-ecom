from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from apps.payments.models import Payment
from apps.payments.api.serializer import CreatePaymentSerializer, PaymentSerializer
from apps.payments.services import create_payment_for_order


class PaymentCreateAPIView(generics.GenericAPIView):
    serializer_class = CreatePaymentSerializer
    permission_classes = [permissions.IsAuthenticated]


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception =True)
        payment = create_payment_for_order(
            user=request.user,
            order_id=serializer.validated_data["order_id"],
            payment_method=serializer.validated_data["payment_method"],

        )
        output_serializer = PaymentSerializer(payment)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class PaymentDetailAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return Payment.objects.filter(order__user=self.request.user).select_related("order")