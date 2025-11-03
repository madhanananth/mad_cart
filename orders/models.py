from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from products.models import Product
from users.models import CustomerProfile,Address

# Create your models here.

class Order(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE )
    billing_address = models.ForeignKey(
        'users.Address',
        on_delete=models.SET_NULL,
        null=True,
        related_name='billing_orders'
    )
    delivery_address = models.ForeignKey(
        'users.Address',
        on_delete = models.SET_NULL,
        null = True,
        related_name = 'delivery_orders'
    )
    ordered_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=50 ,choices=[
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ], default='PENDING')
    
    @property
    def total_price(self):
        return sum(item.quantity * item.price for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    
class OrderItem(models.Model):

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)   
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2 )

    def __str__(self):
        return f"{self.quantity}X {self.product.name}"

