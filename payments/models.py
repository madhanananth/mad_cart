from django.db import models
from orders.models import Order

# Create your models here.
PAYMENT_METHOD_CHOICES = [
    ('credit_card', 'Credit Card'),
    ('upi', 'UPI'),
    ('paypal', 'PayPal'),
    ('netbanking', 'Net Banking'),
]

class Payment(models.Model):

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50,choices=PAYMENT_METHOD_CHOICES)
    paid_at = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"payment for order #{self.order.id} "
    




