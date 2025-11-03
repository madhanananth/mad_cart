from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerProfileViewSet, AddressViewSet

router = DefaultRouter()
router.register(r'', CustomerProfileViewSet, basename='auth')
router.register(r'', AddressViewSet, basename='address')


urlpatterns = [
    path('', include(router.urls)),                      
]