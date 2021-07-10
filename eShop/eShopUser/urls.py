from django.contrib import admin
from django.urls import path
from . import views
from .middlewares.auth import  auth_middleware


urlpatterns = [
    path('', views.Index.as_view(), name='homepage'),
    path('store', views.store , name='store'),
    path('search', views.search_view,name='search'),
    path('add-to-cart/<int:pk>', views.add_to_cart_view,name='add-to-cart'),
    path('cart', auth_middleware(views.Cart.as_view()) , name='cart'),
    path('check-out', views.CheckOut , name='checkout'),

    # Payment APIs
    # path('payment/', views.payment, name = 'payment'),
    path('handlerequest/', views.handlerequest, name = 'handlerequest'),
    # Generating Invoice
    path('my-profile', views.my_profile_view,name='my-profile'),
    path('About-Us', views.aboutUs , name='About-Us'),
    path('orders', auth_middleware(views.OrderView.as_view()), name='orders'),
    path('send-feedback', views.send_feedback_view,name='send-feedback'),
    path('download-invoice/<int:orderID>/<int:productID>', views.download_invoice_view,name='download-invoice'),

]
