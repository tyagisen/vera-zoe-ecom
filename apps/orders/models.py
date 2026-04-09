from django.db import models
from decimal import Decimal
from django.conf import settings
from apps.common.models import BaseModel
from apps.products.models import ProductVariant
from .choices import StatusChoices, PaymentStatusChoices


User = settings.AUTH_USER_MODEL

class Address(BaseModel):
    user = models.ForeginKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 =models.CharField(max_length=255)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    post_code = models.CharField(max_length=30)
    country = models.CharField(max_length=120)
    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ["-is_defualt", "-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.address_line_1}, {self.city}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name="orders")
    status = models.CharField(max_length=20, choices = StatusChoices.choices, default=StatusChoices.PENDING)
    payment_status = models.CharField(max_length=20, choices = PaymentStatusChoices.choices, default=PaymentStatusChoices.UNPAID)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))


    class Meta:
        ordering= ["-created_at"]

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, related_name="order_items")
    product_name = models.CharField(max_length=255)
    sku = models.CharField(max_length=80)
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    total_price = models.DecimalField(max_digits=20, decimal_places=2)


    class Meta:
        ordering=["id"]

    
    def __str__(self):
        return f"{self.product_name}  * {self.quantity}"