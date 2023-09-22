from django.urls import path
from rest_framework import routers
#from rest_framework.urlpatterns import format_suffix_patterns
from . import views


#router = routers.DefaultRouter()
#router.register('', views.blogs,'posts')

urlpatterns = [
    #path('', include(router.urls)),
    path('product/<int:id>', views.product,name='product'), # DELETE, GET, PATCH
    path('get-products/', views.get_products,name='products'),# GET
    path('product/post-images/<int:id>', views.product_image,name='post-product-image'),# POST
    path('add-product/', views.add_product,name='add-product'),# POST

    path('cart/<int:id>', views.cart,name='cart'),# DELETE, GET
    path('get-carts/', views.get_carts,name='carts'),# GET
    path('add-to-cart/<int:id>', views.add_to_cart,name='add-to-cart'),# PATCH
    path('remove-from-cart/<int:id>', views.remove_from_cart,name='remove-from-cart'),# PATCH
]
