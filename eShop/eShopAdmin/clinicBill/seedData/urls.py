from django.urls import path,include
from seedData import views
#from django.conf import settings
#from django.conf.urls.static import static

urlpatterns = [
    path('seeddata',views.admin_seeddata,name='seed_data'),
   
                        
]
