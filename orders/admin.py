from django.contrib import admin
from .models import Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'ordered_at', 'is_paid', 'status', 'total_price']
    readonly_fields = ['total_price']  # ✅ This will show it in the edit page

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
