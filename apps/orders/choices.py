from django.db import models
class StatusChoices(models.TextChoices):
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    PACKED = "packed", "Packed"
    SHIPPED = "shipped", "Shipped"
    DELIVERED = "delivered", "Delivered"
    CANCELLED = "cancelled", "Cancelled"


class PaymentStatusChoices(models.TextChoices):
    UNPAID = "unpaid", "Unpaid"
    PAID = "paid", "Paid"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"