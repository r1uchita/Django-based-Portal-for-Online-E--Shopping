from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import Group,User
from django.conf import settings as conf_set
from django.contrib import messages



# Create your views here.



def admin_seeddata(request):
    user=User.objects.create_user(username="bodhi",email="bodhi.technology@outlook.com",password="bodh73!@techno",first_name="bodhi",last_name="technology",is_superuser="True",is_staff="True",is_active="True")
    user=User.objects.create_user(username="suyash",email="vaishnavi.technology@outlook.com",password="123123123",first_name="Suyash",last_name="Nursing Home")
    user.save()
    return HttpResponse("<h1>data seed sucessfuly....<h1>")



