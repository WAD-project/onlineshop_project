from django.urls import path
from reuse import views
from django.conf.urls import url
from django.conf.urls import include


app_name = 'reuse'

urlpatterns = [
    
path('', views.homepage, name='homepage'),
path('about/', views.about, name='about'),
path('faq/', views.faq, name='faq'),
path('contact_us/', views.contact_us, name='contact_us'),
path('login/', views.user_login, name='login'),
path('register/', views.register, name='register'),
path('logout/', views.user_logout, name='logout'),
path('profile/', views.view_profile, name='profile'),

path('profile/edit_profile/',views.edit_profile, name='edit_profile'),
path('profile/wishlist/', views.wishlist, name='wishlist'),
path('profile/shopping_cart/',views.shoppingcart,name='shoppingcart'),
path('profile/change_password/', views.change_password, name='change_password'),
path('<slug:category_name_slug>/', views.show_category, name='show_category'),
path('<slug:category_name_slug>/<slug:subcategory_name_slug>/',views.show_sub, name='show_sub'),
path('<slug:category_name_slug>/<slug:subcategory_name_slug>/add_product/', views.add_product, name='add_product'),
path('<slug:category_name_slug>/<slug:subcategory_name_slug>/<slug:product_name_slug>/', views.show_product, name='product'),
path('<slug:category_name_slug>/<slug:subcategory_name_slug>/<slug:product_name_slug>/add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),

#path('edit_profile/shopping_cart/check_out',views.checkout,name='checkout'),
#path('edit_profile/history',views.history,name='history'),
#path('edit_profile/sold_products ',views.soldproducts,name='soldproducts'),
#path('edit_profile/current_products_list ',views.currentproducts,name='currentproducts'),
url(r'^ajax_calls/search/', views.autocompleteModel, name='search'),



    
]
