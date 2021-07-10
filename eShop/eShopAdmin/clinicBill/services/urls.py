"""clinicBill URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path,include
from services import views as srviews


urlpatterns = [
    path('services_add',srviews.services_addServ,name='services_servAdd'),
    path('edit_service/<int:id>',srviews.services_editService,name='service_servEdit'),
    path('delete_service/<int:id>',srviews.services_delServ,name='service_servDel'),
    path('services_export_excel',srviews.services_export_xls,name='services_servExportExl'),
   
]
