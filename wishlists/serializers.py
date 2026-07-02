from rest_framework import serializers
from .models import Wishlist
from products.serializers import ProductSerializer
from products.models import Product


class WishlistSerializer(serializers.ModelSerializer):

    product = ProductSerializer( read_only=True )

    class Meta:
         model= Wishlist
         fields = ['id','product','created_at']
         read_only_fields= ['id','created_at']

class WishlistCreateSerializer(serializers.Serializer):
     
     product_id =serializers.IntegerField()

     def validate_product_id(self,value):
          
          if not Product.objects.filter(id =value).exists():
               raise serializers.ValidationError("Product doesn't exist")
          return value