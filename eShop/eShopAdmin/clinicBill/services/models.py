from django.db import models

# Create your models here.


class Service(models.Model):
    name=models.CharField(max_length=50)
    price=models.CharField(max_length=15)    
    submitted_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        db_table:"service"