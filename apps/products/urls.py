from django.urls import path
from apps.products.views import (
    CategoryListAPIView,
    ProductListAPIView,
    FeaturedProductListAPIView,
    ProductDetailAPIView
)

urlpatterns = [
    path("categories/", CategoryListAPIView.as_view(), name="category-list"),
    path("", ProductListAPIView.as_view(), name="product-list"),
    path("featured/", FeaturedProductListAPIView.as_view(), name="featured-product-list"),
    path("<slug:slug>/", ProductDetailAPIView.as_view(), name="product-detail"),
]