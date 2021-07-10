from django.db import  models
# from django.contrib.auth.models import User




class Customer(models.Model):
    # user=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)
    profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)


    def get_name(self):
        return self.first_name

    def __str__(self):
        cust=str(self.first_name)
        return cust

    def get_id(id):
        customer_id=Customer.objects.get(id=id)
        return customer_id
    
    

    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False


    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True

        return  False


