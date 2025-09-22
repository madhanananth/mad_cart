from rest_framework import viewsets, permissions
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from users.models import CustomerProfile


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer__user=self.request.user).order_by('-ordered_at')

    def perform_create(self, serializer):
        customer_profile = CustomerProfile.objects.get(user=self.request.user)
        serializer.save(customer=customer_profile)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(order__customer__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

# Create your views here.

# class OrderItemViewSet(viewsets.ModelViewSet):

#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemSerializer

# class OrderViewSet(viewsets.ModelViewSet):

#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer


