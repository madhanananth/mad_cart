from rest_framework import viewsets, permissions,status
from .models import Order, OrderItem
from cart.models import Cart
from users.models import Address 
from products.models import Product
from rest_framework.response import Response
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-ordered_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    # create order from cart
    @action(detail=False , methods=['post'],url_path='from_cart')
    def create_from_cart(self,request):

        user= request.user
        billing_address_id = request.data.get('billing_address')
        delivery_address_id = request.data.get('delivery_address')
        try:
            billing_address = Address.objects.get(id=billing_address_id, customer=user)
            delivery_address = Address.objects.get(id=delivery_address_id, customer=user)
        except Address.DoesNotExist:
            return Response({'error': 'Invalid address provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = Cart.objects.get(user=user)

        except Cart.DoesNotExist:
            return Response({'Detail' : 'Cart not found'},status= status.HTTP_404_NOT_FOUND)
        
        if not cart.items.exists() :

            return Response({'Detail' : 'Cart item is Empty' },status=status.HTTP_400_BAD_REQUEST)
        
        # Create order

        order = Order.objects.create(
            user=user,
            billing_address= billing_address,
            delivery_address= delivery_address,
            is_paid = False,
            status= 'PENDING'
        )
        
        # add all cart items to order

        for item in cart.items.all():

            OrderItem.objects.create(
                order=order,
                product = item.product,
                quantity =item.quantity,
                price = item.product.price
            )

        cart.items.all().delete()

        return Response(OrderSerializer(order).data , status=status.HTTP_201_CREATED)
    

    # create order from a single product
    @action(detail=False, methods=['post'], url_path='buy_now')
    def buy_now(self, request):

        user= request.user
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity,1'))
        billing_address_id = request.data.get('billing_address')
        delivery_address_id = request.data.get('delivery_address')

        if not product_id :

            return Response({'Detail' : 'Product_id is Required'}, status=status.HTTP_400_BAD_REQUEST)
        

        product = get_object_or_404(Product, id = product_id)

        #create order 

        order = Order.objects.create(
            user= user,
            delivery_address_id=delivery_address_id,
            billing_address_id=billing_address_id,
            is_paid = False,
            status = 'PENDING'
        )

        # Add product as orderItem 
        OrderItem.objects.create(
            product=product,
            quantity=quantity, 
            price = product.price,
        )

        return Response(OrderItemSerializer(order).data, status=status.HTTP_201_CREATED)
            





