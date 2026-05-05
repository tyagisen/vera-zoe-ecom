from decimal import Decimal
from uuid import uuid4
from django.db import transaction
from rest_framework.exceptions import ValidationError
from apps.cart.models import Cart
from apps.orders.models import Address, Order, OrderItem

@transaction.atomic
def create_order_from_cart(*, user, address_id):
    try:
        address = Address.objects.get(id=address_id, user=user)
    except Address.DoesNotExist:
        raise ValidationError({"address_id": "Invalid address for this user"})

    cart = {
        Cart.objects.select_related("user")
        .prefetch_related("items__variant__product")
    }
    cart_items = list(cart.items.all())
    if not cart_items:
        raise ValidationError({"cart":"Cart is Empty"})
    subtotal = Decimal("0.00")
    order = Order.objects.create(
        user = user,
        address=address,
        order_number = f"VZ-{uuid4().hex[:10].upper()}",
        shipping_cost = Decimal("0.00"),
        tax= Decimal("0.00"),
        subtotal=Decimal("0.00"),
        total = Decimal("0.00"),
    )
    order_items = []
    for cart_item in cart_items:
        variant = cart_item.variant

        if not variant.is_active:
            raise ValidationError({"variant":f"Variant {variant.id} is inactive"})
        
        if cart_item.quantity > variant.stock:
            raise ValidationError(
                {"Stock": f"Not Enough stock for {variant.product.name} ({variant.size}, {variant.color})."}

            )
        unit_price = variant.final_price
        line_total = unit_price*cart_item.quantity
        subtotal  += line_total
        
        order_items.append(
            OrderItem(
                order=order,
                variant=variant,
                product_name=variant.product.product_name,
                sku = variant.sku,
                size= variant.size,
                color = variant.color,
                quantity = cart_item.quantity,
                unit_price = unit_price,
                line_total=line_total,
            )
        )
        variant.stock-=cart_item.quantity
        variant.save(update_fields=["stock","updated_at"])
    OrderItem.objects.bulk_create(order_items)
    order.subtotal = subtotal+order.shipping_cost
    order.save(update_fields = ["subtotal", "total", "updated_at"])
    cart.items.all().delete()
    return order