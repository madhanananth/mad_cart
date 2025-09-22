from .views import ProductViewSet, CategoryViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path,include


router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]
