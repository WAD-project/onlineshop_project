from django.urls import path
from reuse import views

app_name = 'reuse'

urlpatterns = [
    
    path('', views.homepage, name='homepage'),
    
]
