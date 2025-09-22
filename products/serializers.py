from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
     class Meta:
          model = Category
          fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
     category_detail = CategorySerializer(source='category', read_only=True)
     category_name = serializers.CharField(source='category.name', read_only=True)

     class Meta: 
          model = Product
          fields = ['id', 'name', 'description', 'price', 'stock', 'image', 'created_at', 'category','category_detail', 'category_name']    