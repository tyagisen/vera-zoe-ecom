from django.urls import path
from apps.payments.views import PaymentCreateAPIView, PaymentDetailAPIView

urlpatterns = [
    path("create/", PaymentCreateAPIView.as_view(), name="payment-create"),
    path("<int:pk>/", PaymentDetailAPIView.as_view(), name="payment-detail")
]