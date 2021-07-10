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
from patient import views as pviews


urlpatterns = [
   path('Dashboard',pviews.dashboard_dash,name='dashboard'),
   path('register_patient',pviews.patient_register,name='patient_addp'),
   path('list_patient',pviews.patient_listp,name='patient_list'),
   path('edit_patient/<int:id>',pviews.patient_editPatient,name='patient_edit'),
   path('delete_patient/<int:id>',pviews.patient_delpatient,name='patient_del'),
   path('excelexport_patient',pviews.patient_export_xls,name='patient_expoxls'),
]
