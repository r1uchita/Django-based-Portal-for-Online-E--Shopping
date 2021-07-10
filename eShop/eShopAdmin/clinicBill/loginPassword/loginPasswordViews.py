from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import Group,User
from django.conf import settings as conf_set
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django import template
from socket import gaierror
from smtplib import SMTPAuthenticationError, SMTPDataError
from loginPassword.loginPasswordForms import LoginForm

# Create your views here.
sname=conf_set.C_NAME


def login(request):
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            userName=loginForm.cleaned_data['username']
            userPassword=loginForm.cleaned_data['passwd']
            try:
                user=auth.authenticate(username=userName,password=userPassword)
                if user is not None:
                    auth.login(request,user)
                    request.session['username']=userName
                    return redirect('dashboard')
                else:
                    messages.error(request,'Invalid credentials.... try again')
                    return redirect('login')    
            except:
                messages.error(request,'Invalid header found at login.... try again')
                return redirect('login')       
        else:
            messages.error(request, 'Not valid Login...')
    else:
        loginForm = LoginForm()
    context = {'loginForm': loginForm,'sname':sname}    
    return render(request, 'loginPasswd/login.html',context) 
   




def logout(request):
    try:
        del request.session['username']
        auth.logout(request)
        return redirect('login')
    except KeyError:
        messages.error(request, 'Session Timeout!....')
        return redirect("login")    




def change_password(request):
    if request.session.has_key('username'):
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
        return render(request, 'loginPasswd/changepass.html',context) 
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
					email_template_name = "loginPasswd/password_reset_email.txt"
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
						send_mail(subject, email, 'infomindsbodhi@gmail.com' , [user.email], fail_silently=False)
					except(BadHeaderError,gaierror,SMTPAuthenticationError,SMTPDataError):
						messages.error(request,'Email Not Send... try again');return redirect('password_reset')
					messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
					return redirect ('login')
			else:messages.error(request, 'An invalid email has been entered.');return redirect('password_reset')
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="loginPasswd/password_reset_form.html", context={"password_reset_form":password_reset_form})