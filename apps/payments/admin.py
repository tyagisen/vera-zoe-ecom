from django.contrib import admin

from apps.payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'order',
        'payment_method',
        'provider',
        'amount',
        'status',
        'paid_at',
        'created_at',
    ]
    list_filter=("payment_method", "provider", "status")
    search_fields = ("order__order_number", "transaction_id")
    readonly_fields = ("created_at", "updated_at")