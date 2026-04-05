from django.urls import path
from apps.cart.views import (
    CartAPIView,
    AddToCartAPIView,
    UpdateCartItemAPIView,
    RemoveCartItemAPIView,
)

urlpatterns = [

    path("", CartAPIView.as_view(), name="cart"),
    path("add/", AddToCartAPIView.as_view(), name="add-to-cart"),
    path("item/<int:pk>/", UpdateCartItemAPIView.as_view(), name="update-cart-item"),
    path("item/<int:pk>/delete/", RemoveCartItemAPIView.as_view(), name="remove-cart-item")
]