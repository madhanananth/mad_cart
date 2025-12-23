from .views import SearchViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path,include


router = DefaultRouter()
router.register(r'', SearchViewSet, basename='search')


urlpatterns = [
    path('', include(router.urls)),
]
