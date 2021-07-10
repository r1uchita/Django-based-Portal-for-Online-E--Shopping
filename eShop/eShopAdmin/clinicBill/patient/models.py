from django.db import models

# Create your models here.

class PatientRegister(models.Model):
    name=models.CharField(max_length=50)
    dob=models.CharField(max_length=15,null=True)    
    gender=models.CharField(max_length=8) 
    mobile=models.CharField(max_length=12)
    email=models.CharField(max_length=50,null=True)
    address=models.CharField(max_length=200,null=True)
    photo=models.ImageField(upload_to="patient/imgs",null=True)
    submitted_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        db_table:"p_register"
