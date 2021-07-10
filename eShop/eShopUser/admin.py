from django.contrib import admin
from .models.orders import Order
from .models.category import Category
from .models.customer import Customer
from .models.product import Product
from .models.feedback import Feedback
# from django.contrib import admin
# from .models import Customer,Product,Orders,Feedback
# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','phone','email','password','profile_pic']    
admin.site.register(Customer, CustomerAdmin)

class AdminCategory(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Category , AdminCategory)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category','image']
admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['product','quantity', 'price', 'customer','phone','address','date','status','total_amount','payment_status','datetime_of_payment','razorpay_order_id','razorpay_payment_id','razorpay_signature']
admin.site.register(Order, OrderAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name','feedback','date']
admin.site.register(Feedback, FeedbackAdmin)
# Register your models here.



# class AdminProduct(admin.ModelAdmin):
#     list_display = ['name', 'price', 'category','image']




# class AdminOrder(admin.ModelAdmin):
#     list_display = ['product','quantity', 'price', 'customer','phone','address','date','status']



# class AdminCategory(admin.ModelAdmin):
#     list_display = ['name']


# class AdminCustomer(admin.ModelAdmin):
#     list_display = ['first_name','phone','email','password']    


# # Register your models here.
# admin.site.register(Product, AdminProduct)
# admin.site.register(Category , AdminCategory)
# admin.site.register(Customer,AdminCustomer )
# admin.site.register(Order,AdminOrder)
