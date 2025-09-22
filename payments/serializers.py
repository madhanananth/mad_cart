from rest_framework import serializers
from .models import Payment
from orders.models import Order



class PaymentSerializer(serializers.ModelSerializer):

    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    paid_at = serializers.DateTimeField(read_only = True)

    class Meta:
        model = Payment
        fields =  [
            'id',
            'order',
            'payment_method',
            'paid_at',
            'is_successful',
            'transaction_id',
        ]