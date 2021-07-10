from django.db import models
from .product import Product
from .customer import Customer
import datetime
from django.utils.timezone import now


class Order(models.Model):
    STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )

    payment_status_choices = (
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
    )

    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=150, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status=models.CharField(max_length=50,null=True,choices=STATUS, default='Pending')
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None) 
    total_amount = models.FloatField(default=0, blank=True)
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
    datetime_of_payment = models.DateTimeField(default=now)
    # related to razorpay
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)
    
    # def save(self, *args, **kwargs):
    #     if self.order_id is None and self.datetime_of_payment and self.id:
    #         self.order_id = self.datetime_of_payment.strftime('PAY2ME%Y%m%dODR') + str(self.id)
    #     return super().save(*args, **kwargs)

    def __str__(self):
        return self.customer.email + " " + str(self.id)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')

