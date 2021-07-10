from django.urls import path,include
from django.contrib.auth import views 
from eShopLoginPassword import views as lpv




urlpatterns = [
   #login,logout
   path('signup', lpv.Signup.as_view(), name='signup'),
   path('login', lpv.Login.as_view(), name='login'),
   path('logout', lpv.logout , name='logout'),
   
   #Password reset urls
   path('changepass',lpv.change_password,name='change_password'),
   path("password_reset", lpv.password_reset_request, name="password_reset"),
   path('password_reset/done/', views.PasswordResetDoneView.as_view(template_name='eShopLoginPassword/password_reset_done.html'), name='password_reset_done'),
   path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(template_name='eShopLoginPassword/password_reset_confirm.html'), name='password_reset_confirm'),
   path('reset/done/', views.PasswordResetCompleteView.as_view(template_name='eShopLoginPassword/password_reset_complete.html'), name='password_reset_complete'),
                            
]
