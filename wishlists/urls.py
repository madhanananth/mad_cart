from .views import WishlistViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', WishlistViewSet, basename='wishlist')

urlpatterns = [
    path('', include(router.urls)),
]