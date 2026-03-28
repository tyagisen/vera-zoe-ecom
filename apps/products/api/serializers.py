from rest_framework import serializers
from apps.products.models import Category, Brand, Product, ProductImage, ProductVariant

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug", 
            "description",
            "image"
        ]

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields= [
            "id",
            "slug",
            "description",
            "logo",

        ]

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields=[
            "id",
            "image",
            "alt_text",
            "is_primary",
            "display_order"
        ]
    


class ProductVariantSerializer(serializers.ModelSerializer):
    final_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    is_in_stock = serializers.BooleanField(read_only=True)
    class Meta:
        model =ProductVariant
        fields = [
            "id",
            "size",
            "color",
            "sku",
            "stock",
            "price_override",
            "final_price",
            "is_active",
            "is_in_stock",
        ]

class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_stock = serializers.IntegerField(read_only=True)
    has_discount = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", 
            "name",
            "slug",
            "category",
            "brand",
            "base_price",
            "discount_price",
            "current_price",
            "has_discount",
            "is_featured",
            "main_image",
            "total_stock",
        ]

class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    image = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_stock = serializers.IntegerField(read_only=True)
    has_discount = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "brand",
            "description",
            "base_price",
            "discount_price",
            "current_price",
            "has_discount",
            "is_active",
            "is_available",
            "is_featured",
            "main_image",
            "total_stock",
            "images",
            "variants",
            "created_at",
            "updated_at",
        ]
