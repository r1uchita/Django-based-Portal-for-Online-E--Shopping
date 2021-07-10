from decimal import Context
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import Group,User
from django.conf import settings as conf_set
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import  check_password
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django import template
from socket import gaierror
from smtplib import SMTPAuthenticationError, SMTPDataError
from eShopUser.models.customer import Customer
from django.views import View
import os

# Create your views here.
sname = conf_set.C_NAME

class Signup(View):
    def get(self, request):
        context={
            'sname':sname,
            }
        return render(request, 'eShopLoginPassword/login.html',context)

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        profile_pic = request.FILES['avatar']
        # img_extension = os.path.splitext(profile_pic.name)[1]
        # user_folder = 'media/profile_pic/CustomerProfilePic/'
        # if not os.path.exists(user_folder):
        #     os.mkdir(user_folder)
        # img_save_path = ("")+ user_folder+profile_pic.name
        # with open(img_save_path, 'wb+') as f:
        #     for chunk in profile_pic.chunks():
        #         f.write(chunk)
        # img = request.FILES['avatar']
        # # img_extension = os.path.splitext(img.name)[1]
        # user_folder = 'media/profile_pic/CustomerProfilePic/'
        # if not os.path.exists(user_folder):
        #     os.mkdir(user_folder)
        # img_save_path = ("")+ user_folder+img.name
        # with open(img_save_path, 'wb+') as f:
        #     for chunk in img.chunks():
        #         f.write(chunk)
        # validation
        value = {
            'first_name': first_name,
            'phone': phone,
            'email': email,
            'profile_pic':profile_pic,
        }
        error_message = None

        customer = Customer(first_name=first_name,
                            phone=phone,
                            email=email,
                            password=password,
                            profile_pic=profile_pic)
        error_message = self.validateCustomer(customer)

        if not error_message:
            print(first_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value,
                'sname':sname,
            }
            return render(request, 'eShopLoginPassword/login.html', data)


    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "First Name Required !!"
        elif len(customer.first_name) < 4:
            error_message = 'First Name must be 4 char long or more'
        # elif not customer.last_name:
        #     error_message = 'Last Name Required'
        # elif len(customer.last_name) < 4:
        #     error_message = 'Last Name must be 4 char long or more'
        elif not customer.phone:
            error_message = 'Phone Number required'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message




class Login(View):
    return_url = None
    def get(self , request):
        Login.return_url = request.GET.get('return_url')
        context={
            'sname':sname,
        }
        return render(request , 'eShopLoginPassword/login.html',context)


    def post(self , request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                error_message = 'Email or Password invalid !!'
        # elif request.is_superuser:
        #     flag = check_password(password, request.password)
        #     if flag:
        #         request.session['customer']= customer.id

        #         if Login.return_url:
        #             return HttpResponseRedirect(Login.return_url)
        #         else:
        #             Login.return_url = None
        #             return redirect('Admin-Dashboard')
        
        else:
            error_message = 'Email or Password invalid !!'

        print(request.user)
        context={
            'sname':sname,
            'error': error_message,
        }
        return render(request, 'eShopLoginPassword/login.html',context)

def logout(request):
    request.session.clear()
    return redirect('login')

#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,CUSTOMER
# def afterlogin_view(request):
#     if Signup.is_customer(request.customer):
#         return redirect('homepage')
#     else:
#         return redirect('admin-dashboard')


# def login(request):
#     if request.method == 'POST':
#         loginForm = LoginForm(request.POST)
#         if loginForm.is_valid():
#             userName=loginForm.cleaned_data['username']
#             userPassword=loginForm.cleaned_data['passwd']
#             try:
#                 user=auth.authenticate(username=userName,password=userPassword)
#                 if user is not None:
#                     auth.login(request,user)
#                     request.session['username']=userName
#                     return redirect('dashboard')
#                 else:
#                     messages.error(request,'Invalid credentials.... try again')
#                     return redirect('login')    
#             except:
#                 messages.error(request,'Invalid header found at login.... try again')
#                 return redirect('login')       
#         else:
#             messages.error(request, 'Not valid Login...')
#     else:
#         loginForm = LoginForm()
#     context = {'loginForm': loginForm,'sname':sname}    
#     return render(request, 'eShopLoginPassword/login.html',context)


# def logout(request):
#     try:
#         del request.session['username']
#         auth.logout(request)
#         return redirect('login')
#     except KeyError:
#         messages.error(request, 'Session Timeout!....')
#         return redirect("login")    




def change_password(request):
    if request.session.has_key('email'):
        lname=request.user.last_name 
        fname=request.user.first_name
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password has been changed successfully!')
                return redirect('change_password')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = PasswordChangeForm(request.user)
        context = {
            'sname':sname,
            'lname':lname,
            'page_title':"Change Password /",
            'fname':fname,
            "page_path":" ChangePassword",
            "menu_icon":"nav-icon fa fa-shield-alt",
            "form":form
            }    
        return render(request, 'eShopLoginPassword/changepass.html',context) 
    else:
        return redirect('login')        



def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "eShopLoginPassword/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'shadowball3460sb@gmail.com' , [user.email], fail_silently=False)
					except(BadHeaderError,gaierror,SMTPAuthenticationError,SMTPDataError):
						messages.error(request,'Email Not Send... try again');return redirect('password_reset')
					messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
					return redirect ('login')
			else:messages.error(request, 'An invalid email has been entered.');return redirect('password_reset')
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="eShopLoginPassword/password_reset_form.html", context={"password_reset_form":password_reset_form})