from django.urls import path
from reuse import views

app_name = 'reuse'

urlpatterns = [
    
    path('', views.homepage, name='homepage'),
    path ('add_product/', views.add_product, name='add_product'),
    path('register/', views.register, name='register'),
 
    
]
