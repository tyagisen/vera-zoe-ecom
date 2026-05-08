from django.db import models
from decimal import Decimal
from apps.common.models import BaseModel
from apps.orders.models import Order


class Payment(BaseModel):
    from .choices import PaymentMethodChoices, ProviderChoices, StatusChoices
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    payment_method = models.CharField(max_length=30, choices=PaymentMethodChoices.choices,default= PaymentMethodChoices.CARD)
    provider = models.CharField(max_length=30, choices = ProviderChoices.choices, default=ProviderChoices.MANUAL)
    transaction_id = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    status = models.CharField(
        max_length=20, 
        choices=StatusChoices.choices,
        default= StatusChoices.PENDING
    )
    paid_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering=["-created_at"]

    def __str__(self):
        return f"Payment for {self.order.order_number}-{self.status}"
