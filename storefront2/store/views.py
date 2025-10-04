from django.shortcuts import get_object_or_404,get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product , Collection , OrderItem, Order, Review,Cart,CartItem
from rest_framework import status
from django.db.models import Count  , Prefetch
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin ,RetrieveModelMixin,DestroyModelMixin
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from .serializers import ProductSerializer,CollectionSerializer,ReviewSerializer,CartSerializer,CartCartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer
from .filters import ProductFilter
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
# Create your views here.

class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    filter_backends=[DjangoFilterBackend,SearchFilter]
    filterset_class=ProductFilter
    pagination_class=PageNumberPagination
    search_fields=['title','description']


    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count()>0:
            return Response({'error':'Product cannot be deleted because it is associated with an order item.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    

class CollectionViewSet(ModelViewSet):

    queryset=Collection.objects.annotate(total_products=Count('product')).all()
    serializer_class=CollectionSerializer

    def destroy(self, request, *args, **kwargs):

        if self.get_object().product_set.count()>0:
            return Response({'error':'Collection cannot be deleted because it is associated with an order item.'},status=status.HTTP_405_METHOD_NOT_ALLOWED) 
        return super().destroy(request, *args, **kwargs)

   

class ReviewViewSet(ModelViewSet):
    serializer_class=ReviewSerializer
    def get_queryset(self):
        return  Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}

class CartViewSet(
                   CreateModelMixin,RetrieveModelMixin,
                   DestroyModelMixin,GenericViewSet):
    #queryset=Cart.objects.prefetch_related('items__product')
    queryset=Cart.objects.prefetch_related(Prefetch('items',queryset=CartItem.objects.select_related('product__collection__featured_product'))).all()
    serializer_class=CartSerializer

class CartItemViewSet(ModelViewSet):
    http_method_names=['get','post','patch','delete']
    def get_serializer_class(self):

        if self.request.method =='POST':
            return AddCartItemSerializer
        elif self.request.method=='PATCH':
            return UpdateCartItemSerializer
        return CartCartItemSerializer
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}
    
    def get_queryset(self):
        return CartItem.objects.filter(cart=self.kwargs['cart_pk']).select_related('product')
    #note we are using the cart_pk _pk is the default and cart is the lookup we give in the urls.pyS