from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LoginView,LogoutView
from eShopAdmin import views as admindash

urlpatterns = [
     path('adminlogin', LoginView.as_view(template_name='eShopLoginPassword/adminlogin.html'),name='adminlogin'),
     path('Admin-Dashboard', admindash.dashboard ,name='dashboard'),
     path('Category', admindash.Category ,name='category'),
     path('Customers', admindash.Customers ,name='customers'),
     path('Product', admindash.Product ,name='product'),
     path('Order', admindash.Order ,name='order'),
]