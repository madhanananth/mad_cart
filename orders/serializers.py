from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from users.serializers import AddressSerializer


# class OrderItemSerializer(serializers.ModelSerializer):
#     product = ProductSerializer(read_only=True)

#     class Meta:
#         model = OrderItem
#         fields = ['id', 'product', 'quantity', 'price']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    item = OrderItemSerializer(many=True, read_only=True )
    customer = serializers.ReadOnlyField(source='customer.user.username')
    billing_address = AddressSerializer(read_only=True)
    delivery_address = AddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'customer',
            'ordered_at',
            'total_price',
            'is_paid',
            'status',
            'billing_address',
            'delivery_address',
            'item.product.name',
        ]

# class OrderItemSerializer(serializers.ModelSerializer):

#     product = ProductSerializer(read_only=True)
#     product_id = serializers.PrimaryKeyRelatedField(
#         queryset=Product.objects.all(),
#         source='product',
#         write_only=True
#     )
#     order_id = serializers.PrimaryKeyRelatedField(
#         queryset=Order.objects.all(), source='order', write_only=True
#     )

#     class Meta:
#         model = OrderItem
#         fields = ['id','order_id','product_id','quantity', 'price']

# class OrderSerializer(serializers.ModelSerializer):
    
#     items= OrderItemSerializer(many=True, read_only=True )

#     class Meta:
#         model = Order
#         fields = [
#             'id',
#             'customer',
#             'billing_address',
#             'delivery_address',
#             'ordered_at',
#             'total_price',
#             'is_paid',
#             'status',
#             'items',
#         ]


