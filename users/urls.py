from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerProfileViewSet,AddressViewSet

router = DefaultRouter()
router.register(r'customers', CustomerProfileViewSet,basename='auth')
router.register(r'addresses', AddressViewSet,basename='address')

urlpatterns = [
    path('', include(router.urls)),
]