from django.urls import path
from reuse import views
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin


app_name = 'reuse'

urlpatterns = [
    
path('', views.homepage, name='homepage'),
path('about/', views.about, name='about'),
path('faq/', views.faq, name='faq'),
path('contact_us/', views.contact_us, name='contact_us'),
path('login/', views.user_login, name='login'),
path('register/', views.register, name='register'),
path('logout/', views.user_logout, name='logout'),
path('seller_manual/', views.seller_manual, name='seller_manual'),
path('<slug:user_name_slug>/', views.view_profile, name='profile'),
path('<slug:user_name_slug>/become_a_seller/', views.become_a_seller, name='become_a_seller'),
path('<slug:user_name_slug>/edit_profile/', views.edit_profile, name='edit_profile'),
path('<slug:user_name_slug>/wishlist/', views.wishlist, name='wishlist'),
path('<slug:user_name_slug>/change_password/', views.change_password, name='change_password'),
path('<slug:user_name_slug>/past_orders/', views.past_orders, name='past_orders'),
path('<slug:user_name_slug>/sold_products/', views.sold_products, name='sold_products'),
path('<slug:user_name_slug>/current_products/', views.current_products, name='current_products'),
path('<slug:category_name_slug>/', views.show_category, name='show_category'),
path('<slug:category_name_slug>/<slug:subcategory_name_slug>/',views.show_sub, name='show_sub'),
path('<slug:category_name_slug>/<slug:subcategory_name_slug>/add_product/', views.add_product, name='add_product'),
path('<slug:category_name_slug>/<slug:subcategory_name_slug>/<slug:product_name_slug>/', views.show_product, name='product'),
path('<slug:category_name_slug>/<slug:subcategory_name_slug>/<slug:product_name_slug>/add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
url(r'^admin/', admin.site.urls),
url(r'^$',views.singIn),
#url(r'^postsign/',views.postsign),


#url(r'^ajax_calls/search/', views.autocompleteModel, name='search'),



    
]
