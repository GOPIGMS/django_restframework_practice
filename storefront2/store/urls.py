from django.urls import path
from . import views

from rest_framework_nested import routers
from pprint import pprint

router = routers.DefaultRouter()

router.register('products',views.ProductViewSet,basename='products')
router.register('collections',views.CollectionViewSet)
router.register('carts',views.CartViewSet)


products_router=routers.NestedDefaultRouter(router,'products',lookup='product')
products_router.register('reviews',views.ReviewViewSet,basename='product-reviews')

cartitem_router=routers.NestedDefaultRouter(router,'carts',lookup='cart')
cartitem_router.register('items',views.CartItemViewSet,basename='cart-item')
 
urlpatterns=router.urls + products_router.urls + cartitem_router.urls
