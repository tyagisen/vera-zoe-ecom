from django.db import models
from decimal import Decimal
from django.conf import settings
from apps.common.models import BaseModel
from apps.products.models import ProductVariant


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

    
