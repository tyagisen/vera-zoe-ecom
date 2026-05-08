from rest_framework.exceptions import ValidationError
from apps.orders.models import Order
from apps.payments.models import Payment


def create_payment_for_order(*, user, order_id, payment_method):
    try:
        order= Order.objects.get(id=order_id, user=user)
    except Order.DoesNotExist:
        raise ValidationError({"order": "Invalid order for this user"})
    if order.status == Order.PaymentStatusChoices.PAID:
        raise ValidationError({"order": "This order is already paid"})

    payment, created = Payment.objects.get_or_create(
        order=order,
        defaults={
            "payment_method": payment_method,
            "amount":order.total,
            "provider": Payment.ProviderChoices.MANUAL,
            "status": Payment.StatusChoices.PENDING,

        }
    )
    if not created:
        payment.payment_method = payment_method
        payment.amount = order.totalpayment.save(update_fields=["payment_method", "amount", "updated_at"])

    return payment
