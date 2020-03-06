from django.urls import path
from reuse import views

app_name = 'reuse'

urlpatterns = [
    
    path('', views.homepage, name='homepage'),
    path ('add_product/', views.add_product, name='add_product'),
    path('register/', views.register, name='register'),
    path ('login/', views.user_login, name="login"),
    path('change_password/',views.change_password, name='change_password'),
    path('edit_profile/',views.edit_profile, name="edit_profile"),
    path('logout/', views.user_logout, name='logout'),
 
    
]
