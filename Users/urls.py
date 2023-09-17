from django.urls import path
from . import views

urlpatterns = [
    path('logout/',views.logout,name="logout"),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('resetpassword/', views.resetPassword, name='resetPassword'),
]