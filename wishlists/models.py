from django.db import models
from django.conf import settings
from products.models import Product

# Create your models here.

class Wishlist(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='wishlist_items'
        )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="wishlisted_by"
    )
    created_at =  models.DateTimeField(auto_now_add=True)
    updated_at =  models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wishlist'
        unique_together = ('user', 'product')
        ordering =['-created_at']
        indexes = [
            models.Index(fields=['user', 'product']),
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.product.name}"