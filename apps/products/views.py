from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework import permissions
from apps.products.api.serializers import CategorySerializer, ProductDetailSerializer, ProductListSerializer
from apps.products.models import Category, Product, ProductImage, ProductVariant
from .filters import ProductFilter
from django.db.models import Prefetch
class CategoryListAPIView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Category.objects.active()
    


class ProductListAPIView(ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = ProductFilter
    search_fields = ["name", "description", "category__name", "brand__name"]
    ordering_fields = ["created_at", "base_price"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return (
            Product.objects.available()
            .select_related("category", "brand")
            .prefetch_related(
                Prefetch(
                    "variants",
                    queryset= ProductVariant.objects.filter(is_active=True),
                ),
                Prefetch(
                    "images", queryset=ProductImage.objects.order_by("display_order", "id"),
                )
            )
        )
    
class FeaturedProductListAPIView(ListAPIView):
    serializer_class= ProductListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return (
            Product.objects.featured()
            .select_related("category", "brand")
            .prefetch_related(
                Prefetch(
                    "variants", queryset=ProductVariant.objects.filter(is_active=True),
                    )
            ).order_by("-created_at")
        )


class ProductDetailAPIView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"


    def get_queryset(self):
        return (
            Product.objects.available()
            .select_related(
                "category", "brand"
            )
            
            .prefetch_related(
                Prefetch("images", queryset=ProductImage.objects.order_by("display_order", "id")),
                Prefetch("variants", queryset=ProductVariant.objects.filter(is_active=True))
            )
        )