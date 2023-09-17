from django.urls import path
from rest_framework import routers
#from rest_framework.urlpatterns import format_suffix_patterns
from . import views


#router = routers.DefaultRouter()
#router.register('', views.blogs,'posts')

urlpatterns = [
    #path('', include(router.urls)),
    #path('<int:id>/', views.blogDetai,name='posts-detail'),
    #path('', views.blogs,name='posts'),
    #path('<int:id>/post_images/', views.post_images,name='posts'),
    path('add-product/', views.add_product,name='add-post'),
]
