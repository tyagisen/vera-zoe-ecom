from rest_framework import serializers
from apps.payments.models import Payment
from apps.payments.choices import PaymentMethodChoices


class CreatePaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(
        choices = Payment.PaymentMethodChoices.choices,
        default = Payment.PaymentMethodChoices.CARD,
    )


class PaymentSerializer(serializers.ModelSerializer):
    order_number= serializers.CharField(source="order.order_number", read_only=True)
    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "order_number",
            "payment_method",
            "provider",
            "transaction_id",
            "amount",
            "status",
            "paid_at",
            "created_at"
        ]
        read_only_fields=[
            "id",
            "order",
            "order_number",
            "provider",
            "transaction_id",
            "amount",
            "status",
            "paid_at",
            "created_at",
        ]