from django.shortcuts import render , redirect , HttpResponseRedirect
from eShopUser.models import orders
from eShopUser.models import product
from . import forms
from eShopUser.models.product import Product
from eShopUser.models.orders import Order
from eShopUser.models.category import Category
from eShopUser.models.customer import Customer
from django.views import View
from django.views.generic import View
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings as conf_set
from eShop import settings
from django.views.decorators.csrf import csrf_exempt

sname=conf_set.C_NAME

# Create your views here.
#---------------------------------------------------------------------------------
#------------------------ PUBLIC CUSTOMER RELATED VIEWS START ---------------------
#---------------------------------------------------------------------------------
def search_view(request):
    # whatever user write in search box we get in query
    categories = Category.get_all_categories()
    query = request.GET['query']
    products=Product.objects.all().filter(name__icontains=query)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # word variable will be shown in html when user click on search button
    word="Searched Result :"

    if request.user.is_authenticated:
        return render(request,'eShopUser/index.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart,'sname':sname,'categories':categories})
    return render(request,'eShopUser/index.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart,'sname':sname,'categories':categories})

# any one can add product to cart, no need of signin

def add_to_cart_view(request,pk):
    products=Product.objects.all()

    #for cart counter, fetching products ids added by customer from cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=1

    response = render(request, 'eShopUser/index.html',{'products':products,'product_count_in_cart':product_count_in_cart})


class Index(View):

    def post(self , request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return redirect('homepage')


    def get(self , request):
        # print()
        context = {        
        'sname':sname,
        }
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}',context)


def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products()

    data = {
        'products': products,
        'categories': categories,
        'sname':sname,
    }

    print('you are : ', request.session.get('email'))
    
    return render(request, 'eShopUser/index.html', data)




class OrderView(View):


    def get(self , request ):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)

        print(orders)
        return render(request , 'eShopUser/orders.html'  , {'orders' : orders,'sname':sname})






# Adding Payment Gateway
import razorpay
razorpay_client = razorpay.Client(auth=(settings.razorpay_id, settings.razorpay_account_id))

from .models import Order

# @login_required
# def payment(request):
#     if request.method == "POST":
#         try:
#             address = request.POST.get('address')
#             phone = request.POST.get('phone')
#             customer = request.session.get('customer')
#             cart = request.session.get('cart')
#             products_in_cart = Order.objects.filter(cart = cart)
#             final_price = 0
#             if(len(products_in_cart)>0):
#                 for product in products_in_cart:
#                     print(cart.get(str(product.id)))
#                     order = Order(customer=Customer(id=customer),product=product,price=product.price,
#                     address=address,phone=phone,quantity=cart.get(str(product.id)),total_amount = 0)
#                     order.save()
#                     final_price = final_price + (product.product.price * product.quantity)
#             else:
#                 return HttpResponse("No product in cart")
#         except:
#             return HttpResponse("No product in cart")

#         order.total_amount = final_price
#         order.save()

#         order_currency = "INR"

#         callback_url = 'http://'+ str(get_current_site(request))+"/handlerequest/"
#         print(callback_url)
#         notes = {'order-type': "basic order from the website", 'key':'value'}
#         razorpay_order = razorpay_client.order.create(dict(amount=final_price*100, currency=order_currency, notes = notes, receipt=order.order_id, payment_capture='0'))
#         print(razorpay_order['id'])
#         order.razorpay_order_id = razorpay_order['id']
#         order.save()
        
#         return render(request, 'eShopUser/payment/paymentsummaryrazorpay.html', {'order':order, 'order_id': razorpay_order['id'], 'orderId':order.order_id, 'final_price':final_price, 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url})
#     else:
#         return HttpResponse("505 Not Found") 



import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

def download_invoice_view(request,orderID,productID):
    order=orders.Order.objects.get(id=orderID)
    productp=product.Product.objects.get(id=productID)
    mydict={
        'sname':sname,
        'orderDate':order.date,
        'customerName':order.customer.get_name(),
        'customerEmail':order.customer.email,
        'customerMobile':order.phone,
        'shipmentAddress':order.address,
        'orderStatus':order.status,

        'productName':productp.name,
        'productImage':productp.image,
        'productPrice':productp.price,
        'productDescription':productp.description,


    }
    return render_to_pdf('eShopUser/download_invoice.html',mydict)

# class CheckOut(View):
def CheckOut(request):        
    if request.method == "POST":
        try:
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            customer = request.session.get('customer')
            cust= Customer.objects.get(id=customer)
            cart = request.session.get('cart')
            final_price=0
            products = Product.get_products_by_id(list(cart.keys()))
            print(address, phone, customer, cart, products)
            if(len(products)>0):
                for product in products:
                    print(cart.get(str(product.id)))
                    order = Order(customer=Customer(id=customer),
                                    product=product,
                                    price=product.price,
                                    address=address,
                                    phone=phone,
                                    quantity=cart.get(str(product.id)),total_amount=0)
                    order.save()
                    final_price = final_price + (order.price * order.quantity)
            else:
                return HttpResponse("No product in cart")
        except:
            return HttpResponse("No product in cart")
        order.total_amount = final_price
        order.save()

        order_currency = 'INR'

        callback_url = 'http://'+ str(get_current_site(request))+"/handlerequest/"
        print(callback_url)
        notes = {'order-type': "basic order from the website", 'key':'value'}
        razorpay_order = razorpay_client.order.create(dict(amount=final_price*100, currency=order_currency, notes = notes, receipt=order.order_id, payment_capture='0'))
        print(razorpay_order['id'])
        order.razorpay_order_id = razorpay_order['id']
        order.save()
        request.session['cart'] = {}
        return render(request, 'eShopUser/payment/paymentsummaryrazorpay.html', {'sname':sname,'cust':cust,'order':order, 'order_id': razorpay_order['id'], 'orderId':order.order_id, 'final_price':final_price, 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url})
    else:
        return HttpResponse("505 Not Found")

from django.core.mail import EmailMultiAlternatives
from io import BytesIO
@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id','')
            signature = request.POST.get('razorpay_signature','')
            params_dict = { 
            'razorpay_order_id': order_id, 
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }
            try:
                order_db = Order.objects.get(razorpay_order_id=order_id)
            except:
                return HttpResponse("505 Not Found")
            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result==None:
                amount = order_db.total_amount * 100   #we have to pass in paisa
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    order_db.payment_status = 1
                    order_db.save()
                    return render(request,'eShopUser/payment/paymentsuccess.html',{'sname':sname})
                   #'''html="{% extends 'layout/userBaseLayout.html' %}{% load static %}{% block content %}<div class='info' style='margin-top: 30px;'><div class='container' style='text-align:center;'><h1>Payment Success</h1><br><h3>Congratulations! You have successfully done the payment. Your order will reach to you in 5 days.</h3></div></div>{% endblock %}"
                   # return HttpResponse(html,{'sname':sname})'''
                   
                except:
                    order_db.payment_status = 2
                    order_db.save()
                    return render(request, 'eShopUser/payment/paymentfailed.html',{'sname':sname})
            else:
                order_db.payment_status = 2
                order_db.save()
                return render(request, 'eShopUser/payment/paymentfailed.html',{'sname':sname})
        except:
            return HttpResponse("505 not found")


class GenerateInvoice(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            order_db = Order.objects.get(id = pk, user = request.customer, payment_status = 1)     #you can filter using order_id as well
        except:
            return HttpResponse("505 Not Found")
        data = {
            'order_id': order_db.order_id,
            'transaction_id': order_db.razorpay_payment_id,
            'user_email': order_db.customer.email,
            'date': str(order_db.datetime_of_payment),
            'name': order_db.customer.get_name(),
            'order': order_db,
            'amount': order_db.total_amount,
            'sname':sname,
        }
        pdf = render_to_pdf('eShopUser/payment/invoice.html', data)
        #return HttpResponse(pdf, content_type='application/pdf')

        # force download
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %(data['order_id'])
            content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

def aboutUs(request):
    return render(request,'eShopUser/cards.html',{'sname':sname})


def my_profile_view(request):
    customer = request.session.get('customer')
    cum= Customer.objects.get(id=customer)
    print(cum)
    return render(request,'eShopUser/my_profile.html',{'cum':cum,'sname':sname})




class Cart(View):
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print(products)
        return render(request , 'eShopUser/cart.html' , {'products' : products,'sname':sname} )


def send_feedback_view(request):
    feedbackForm=forms.FeedbackForm()
    if request.method == 'POST':
        feedbackForm = forms.FeedbackForm(request.POST)
        if feedbackForm.is_valid():
            feedbackForm.save()
            return render(request, 'eShopUser/feedback_sent.html',{'sname':sname})
    return render(request, 'eShopUser/send_feedback.html', {'feedbackForm':feedbackForm,'sname':sname})