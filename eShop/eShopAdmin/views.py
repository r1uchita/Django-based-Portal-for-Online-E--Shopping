from django.shortcuts import redirect,render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
from django.contrib.auth import forms

from django.urls import reverse
from django.contrib import messages
from eShopUser.models import product,customer,orders,category
from django.conf import settings as conf_set
# Create your views here.

sname=conf_set.C_NAME


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @login_required(login_url='adminlogin')
def dashboard(request):
    customercount=customer.Customer.objects.all().count()
    productcount=product.Product.objects.all().count()
    ordercount=orders.Order.objects.all().count()
    categorycount=category.Category.objects.all().count()

    # for recent order tables
    orderp=orders.Order.objects.all()
    ordered_products=[]
    ordered_bys=[]
    for order in orderp:
        ordered_product=product.Product.objects.all().filter(id=order.product.id)
        ordered_by=customer.Customer.objects.all().filter(id = order.customer.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)


    context = {        
        'sname':sname,
        'customercount':customercount,
        'productcount':productcount,
        'ordercount':ordercount,
        'categorycount':categorycount,
        'data':zip(ordered_products,ordered_bys,orderp),
        }
    return render(request,"eShopAdmin/dashboard.html",context)


def Category(request):
    categorycount=category.Category.objects.all().count()
    categories=category.Category.objects.all()
    context = {
        'sname':sname,            
        'categorycount': categorycount,
        'categories':categories,        
        }
    return render(request,"eShopAdmin/Category.html",context) 

# admin view customer table    
def Customers(request):
    customercount=customer.Customer.objects.all().count()
    customers=customer.Customer.objects.all()
    context = {
        'sname':sname,
        'customers':customers,
        'customercount':customercount,

        }
    return render(request,"eShopAdmin/Customers.html",context)



def Product(request):
    productcount=product.Product.objects.all().count()
    productp=product.Product.objects.all()
    context = {
            'sname':sname,
            'productcount':productcount,
            'productp':productp,
            }
    return render(request,"eShopAdmin/product.html",context)


def Order(request):
    ordercount=orders.Order.objects.all().count()
    # for recent order tables
    orderp=orders.Order.objects.all()
    ordered_products=[]
    ordered_bys=[]
    for order in orderp:
        ordered_product=product.Product.objects.all().filter(id=order.product.id)
        ordered_by=customer.Customer.objects.all().filter(id = order.customer.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)

    context = {
            'sname':sname,
            'ordercount':ordercount,
            'data':zip(ordered_products,ordered_bys,orderp),
            }
    return render(request,"eShopAdmin/Order.html",context)

