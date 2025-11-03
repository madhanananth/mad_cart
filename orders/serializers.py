from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product
from products.serializers import ProductSerializer
from users.serializers import AddressSerializer


class OrderItemSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only =True)
    product_id =serializers.PrimaryKeyRelatedField(
        queryset = Product.objects.all(), 
        source='product',
        write_only = True
    )

    class Meta:
        model = OrderItem
        fields = ['id','product','product_id','quantity','price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required = False )
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'ordered_at',
            'total_price',
            'is_paid',
            'status',
            'billing_address',
            'delivery_address',
            'items',
        ]
        read_only_fields = ['user','is_paid','ordered_at','status']

    def create(self, validated_data):
        items_data = validated_data.pop('items',[])
        order= Order.objects.create(**validated_data)

        for item in items_data:
            OrderItem.objects.create(order=order,**item)
        return order    