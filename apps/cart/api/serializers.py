from rest_framework import serializers
from apps.cart.models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source = "variant.product.name", read_only=True)
    size = serializers.CharField(source="variant.size", read_only=True)
    color = serializers.CharField(source="variant.color", read_only=True)
    price = serializers.DecimalField(source="variant.final_price", max_digits=10, decimal_places=2)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)


    class Meta:
        model = CartItem
        fields= [
            "id",
            "variant",
            "product_name",
            "size",
            "color",
            "quantity",
            "price", 
            "total_price"
        ]
    
class AddToCartSerializer(serializers.Serializer):
    variant_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)


class CartSerializer(serializers.ModelSerializer):
    items= CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10,decimal_places=2, read_only=True)

    class Meta:
        model = Cart

        fields = [
            "id", 
            "items",
            "total_price"
        ]