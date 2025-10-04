from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart,CartItem
from .serializers import CartSerializer, CartItemSerializer

# Create your views here  

class CartViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    def get_cart(self,user):
        
        cart, created = Cart.objects.get_or_create(user=user)
        return cart
    
    @action(detail=False, methods=['get'])
    def view(self,request):

        cart = self.get_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    


    @action(detail=False , methods=['post'])
    def add(self,request): 
        cart = self.get_cart(request.user)
        serializer = CartItemSerializer(data = request.data)

        if serializer.is_valid():
            product = serializer.validated_data['product']

            cart_item ,created = CartItem.objects.get_or_create(
                cart=cart , product= product
            )
            return Response(CartSerializer(cart).data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True , methods=['patch'])
    def update_item(self,request,pk=None):

        cart = self.get_cart(request.user)
        try:
            cart_item = CartItem.objects.get(cart=cart, id=pk)
        except(CartItem.DoesNotExist):
            return Response({'Error' :'Cart Item not found.' })
        
        serializer = CartItemSerializer(cart_item, data = request.data ,partial =True)

        if serializer.is_valid():
            quantity = serializer.validated_data['quantity']

            cart_item.quantity = quantity
            cart_item.save()
            print(CartSerializer(cart).data)

            return Response(CartSerializer(cart).data)
        
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True , methods=['delete'])
    def delete_item(self,request,pk=None):
        cart = self.get_cart(request.user)

        try:
            cart_item = CartItem.objects.get(cart=cart, id=pk)
        except(CartItem.DoesNotExist):

            return Response({'Error':'Cart Item not found'})
        cart_item.delete()

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)






