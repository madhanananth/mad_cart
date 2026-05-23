from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import IntegrityError

from products.models import Product
from .serializers import WishlistCreateSErializer, WishlistSerializer
from .models import Wishlist


class WishlistViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistSerializer

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related('product')
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'count': queryset.count(),
            'result': serializer.data
        }, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = WishlistCreateSErializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product_id']

        try:
            product = Product.objects.get(id=product_id)
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=request.user,
                product=product
            )

            if not created:
                return Response(
                    {'detail': 'Product already in wishlist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            response_serializer = WishlistSerializer(wishlist_item)
            return Response(
                response_serializer.data, status=status.HTTP_201_CREATED
            )

        except Product.DoesNotExist:
            return Response(
                {'detail': 'Product Not Found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
    def destroy(self, request, pk=None):
        try:
            wishlist_item = Wishlist.objects.get(id=pk, user=request.user)
            wishlist_item.delete()
            return Response(
                {'detail': 'Item removed from wishlist'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Wishlist.DoesNotExist:
            return Response(
                {'detail': 'Wishlist item not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
    @action(detail=False, methods=['post'])
    def toggle(self, request):
        serializer = WishlistCreateSErializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data['product_id']

        try:
            product = Product.objects.get(id=product_id)
            wishlist_item = Wishlist.objects.filter(
                user=request.user,
                product=product
            ).first()

            if wishlist_item:
                wishlist_item.delete()
                return Response(
                    {
                        'added': False,
                        'detail': 'Removed from wishlist.'
                    },
                    status=status.HTTP_200_OK
                )
            else:
                Wishlist.objects.create(
                    user=request.user,
                    product=product
                )
                return Response({
                    'added': True,
                    'detail': 'Added to wishlist.'
                }, status=status.HTTP_201_CREATED)
            
        except Product.DoesNotExist:
            return Response({
                'detail': 'Product not found.'
            }, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['delete'])
    def clear(self, request):
        deleted_count, _ = Wishlist.objects.filter(user=request.user).delete()

        return Response({
            'detail': f'Removed {deleted_count} items from wishlist.'
        }, status=status.HTTP_200_OK)