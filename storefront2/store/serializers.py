from rest_framework import serializers
from .models import Product, Collection
from decimal import Decimal

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title','total_products']
    total_products=serializers.IntegerField()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','slug','description','inventory','price','price_with_tax','collection']
    price=serializers.DecimalField(max_digits=10,decimal_places=2,source='unit_price')
    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
    def calculate_tax(self,product:Product):
        return product.unit_price * Decimal('1.1')

