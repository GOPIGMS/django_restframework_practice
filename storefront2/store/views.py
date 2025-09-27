from django.shortcuts import get_object_or_404,get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer,CollectionSerializer
from .models import Product , Collection
from rest_framework import status
from django.db.models import Count  

# Create your views here.
@api_view(['GET','POST'])
def product_list(request):
    if request.method == 'POST':
        serializer=ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
      

    if request.method == 'GET':
        products=Product.objects.select_related('collection').all()
        serializedData = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializedData.data,status=status.HTTP_200_OK)


@api_view(['GET','PUT','PATCH','DELETE'])
def product_detail(request, pk):
   
    product= get_object_or_404(Product.objects.select_related('collection'),id=pk)
    
    if request.method == 'GET':
        serializedData = ProductSerializer(product, context={'request': request})
        return Response(serializedData.data)
    if request.method =='PUT':
        serializedData=ProductSerializer(product,data=request.data)
        serializedData.is_valid(raise_exception=True)
        serializedData.save()
        return Response (serializedData.data,status=status.HTTP_201_CREATED)
    if request.method =='PATCH':
        serializedData=ProductSerializer(product,data=request.data,partial=True)
        serializedData.is_valid(raise_exception=True)
        serializedData.save()
        return Response (serializedData.data,status=status.HTTP_201_CREATED)
    if request.method =='DELETE':
        if product.orderitem_set.count()>0:
            return Response({'error':'Product cannot be deleted because it is associated with an order item.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','PUT','DELETE'])
def collection_detail(request,pk):
    collection= get_object_or_404(Collection.objects.annotate(total_products=Count('product')),id=pk)
    if request.method== 'GET':
        
        serializedData = CollectionSerializer(collection, context={'request': request})
        return Response(serializedData.data)
    if request.method == 'PUT':
        serialized = CollectionSerializer(collection,data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response (serialized.data,status=status.HTTP_200_OK)
    if request.method =='PATCH':
        serialized= CollectionSerializer(collection,data=request.data,partial=True)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response(serialized.data,status=status.HTTP_200_OK)
    if request.method =='DELETE':
        if collection.product_set.count()>0:
            return Response({'error':'Collection cannot be deleted because it is associated with an order item.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        


@api_view(['GET','POST'])
def collection_list(request):
    if request.method == 'GET':
        collections=get_list_or_404(Collection.objects.annotate(total_products=Count('product')))
        serializedData = CollectionSerializer(collections, many=True, context={'request': request})
        return Response(serializedData.data,status=status.HTTP_200_OK)
    if request.method =='POST':
        serializedData =CollectionSerializer(data=request.data)
        serializedData.is_valid(raise_exception=True)
        serializedData.save()
        return Response(serializedData.data,status=status.HTTP_201_CREATED)
    

