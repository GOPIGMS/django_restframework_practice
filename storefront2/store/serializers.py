from rest_framework import serializers
from .models import Product, Collection,Review,Cart,CartItem
from decimal import Decimal


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title','total_products']
    total_products=serializers.IntegerField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','slug','description','inventory','price','price_with_tax','collection']
    price=serializers.DecimalField(max_digits=10,decimal_places=2,source='unit_price')
    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
    def calculate_tax(self,product:Product):
        return product.unit_price * Decimal('1.1')
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['id','name','description','date']
    def create(self, validated_data):
        product_id=self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)

class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','inventory','unit_price']

class CartCartItemSerializer(serializers.ModelSerializer):
    product=CartProductSerializer()
    item_price=serializers.SerializerMethodField()
    def get_item_price(self,obj:CartItem):
        return obj.product.unit_price * obj.quantity
    class Meta:
        model=CartItem
        fields=['id','product','quantity','item_price']      


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id= serializers.IntegerField()

    def validate_product_id(self,value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product for the given id was found.')
        return value

    def save(self, **kwargs):
        cart_id=self.context['cart_id']
        product_id=self.validated_data['product_id']
        quantity= self.validated_data['quantity']
        try:
            cart_item= CartItem.objects.get(cart_id=cart_id,product_id=product_id)
            cart_item.quantity+=quantity
            cart_item.save()
            self.instance=cart_item
        except CartItem.DoesNotExist:
            self.instance= CartItem.objects.create(cart_id=cart_id,**self.validated_data)
        return self.instance
            
    class Meta:
        model=CartItem
        fields=['id','product_id','quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
 
    quantity=serializers.IntegerField()
    class Meta:
        model=CartItem
        fields=['quantity']
 

class CartSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    items=CartCartItemSerializer(many=True,read_only=True)
    total_price= serializers.SerializerMethodField()
    def get_total_price(self,obj:Cart):
        
        return sum([curitem.product.unit_price * curitem.quantity for curitem in obj.items.all() ])
    class Meta:
        model=Cart
        fields=['id','items','total_price']



    


