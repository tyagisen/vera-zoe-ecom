from django.db import models


class PaymentMethodChoices(models.TextChoices):
    CARD= "card","Card"
    CASH_ON_DELIVERY ="cash_on_delivery", "Cash on Delivery"
    BANK_TRANSFER = "bank_transfer", "Bank Transfer"


class ProviderChoices(models.TextChoices):
    STRIPE = "stripe", "Stripe"
    MANUAL = "manual", "Manual"
    CASH = "cash", "Cash"


class StatusChoices(models.TextChoices):
    PENDING= "pending", "Pending"
    PAID = "paid", "Paid"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"
