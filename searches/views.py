from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q ,Count
from products.models import Product
from products.serializers import ProductSerializer
from .models import SearchHistory



# Create Search ViewSet

class SearchViewSet(viewsets.ViewSet):

    permission_classes=[IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='products')
    def search_products(self, request):

        query = request.GET.get('q','')
        results = []

        if query:

            if request.user.is_authenticated :
                SearchHistory.objects.create(user= request.user ,query=query)

            products = Product.objects.filter(
                Q(name__icontains= query ) |
                Q(description__icontains= query) |
                Q(category__name__icontains = query)
            ).distinct()

            results = ProductSerializer(products, many=True).data

        return Response({'query': query, 'results':results})
    
    
    @action(detail=False, methods=['get'], url_path='popular')
    def popular_searches(self, request):
        popular = (
            SearchHistory.objects.values('query')
            .annotate(count=Count('query'))
            .order_by('-count')[:5]
        )
        return Response(list(popular))