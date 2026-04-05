from django.db import models
from apps.products.models import ProductVariant
from apps.common.models import BaseModel
from django.conf import settings

User = settings.AUTH_USER_MODEL
# Create your models here.
class Cart(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"Cart of {self.user}"
    

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    class Meta:
        unique_together= ("cart", "variant")

    def __str__(self):
        return f"{self.variant} * {self.quantity}"

    @property
    def total_price(self):
        return self.quantity * self.variant.final_price