from django.urls import path
from apps.orders.views import AddressListCreateAPIView, OrderCreateAPIView, OrderDetailAPIView, OrderListAPIView
urlpatterns = [
    path("address/", AddressListCreateAPIView.as_view(), name= "address-list-create"),
    path("", OrderListAPIView.as_view(), name="order-list"),
    path("create/", OrderCreateAPIView.as_view(), name="order-create"),
    path("<int:pk>/", OrderDetailAPIView.as_view(), name="order-detail")
]