from rest_framework import serializers
from apps.orders.models import Address, Order, OrderItem

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        models = Address
        fields = [
            "id",
            "full_name",
            "phone_number",
            "address_line_1",
            "address_line_2", 
            "city",
            "state",
            "postcode",
            "country",
            "is_default",
        ]

class CreateOrderSerializer(serializers.Serializer):
    address_id= serializers.IntegerField()


class OrderItemSerailizer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "product_name",
            "sku",
            "size",
            "color",
            "quantity",
            "unit_price",
            "total_price",
        ]
    

class OrderSerailizer(serializers.ModelSerializer):
    items = OrderItemSerailizer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "status",
            "payment_status",
            "subtotal",
            "shipping_code",
            "tax",
            "total",
            "address",
            "items",
            "created_at",
        ]
