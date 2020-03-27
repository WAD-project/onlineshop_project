from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from reuse.models import Category, Subcategory, Product, CurrentProduct, UserProfile, Wishlist, SoldProduct
from reuse.forms import ProductForm, UserForm, UserProfileForm,  UserUpdateForm, ProfileUpdateForm, SellerForm
from django.db.models import Q
from reuse.decorators import user_is_seller

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import JsonResponse

# Create your views here.

def homepage(request):
    category_list = Category.objects.order_by('name')
    context_dict = {}
    context_dict['title'] = 'Welcome'
    context_dict['categories'] = {}
    for cat in category_list:
        context_dict['categories'][cat] = Subcategory.objects.filter(category=cat).order_by('name')
        
    #context_dict['recently'] = CurrentProduct.objects.order_by('date')[5]
    
    query = ""
    if request.GET:
        query = request.GET['q']
        context['query'] = str(query)
    
    product_posts = sorted(get_shop_queryset(query), key=attrgetter('date_uploaded', reverse=True))
    context['product_posts']=product_posts
    
    response = render(request, 'reuse/homepage.html', context = context_dict)
    return response

def about(request):
    return render(request,'reuse/about.html')

def faq(request):
    return render(request, 'reuse/faq.html')
    
def contact_us(request):
    # Add stuff here
    return render(request, 'reuse/contact_us.html')
 
"""
Register
"""
def register(request):
    context_dict = {}
    context_dict['title'] = 'Join Re*'
    
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
            
            wishlist = Wishlist(user=profile)
            wishlist.save()
        else:
            print(user_form.errors, profile_form.errors)
            
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    context_dict['user_form'] = user_form
    context_dict['profile_form'] = profile_form
    context_dict['registered'] = registered
    return render(request, 'reuse/register.html', context_dict)

"""
Edit profile view 
"""
@login_required 
def edit_profile(request, user_name_slug):
    #This is for the mega menu at the navbar
    context_dict = {}

    #edit_profile 
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            user_form =form.save()
            custom_form = profile_form.save(commit=False)
            custom_form.user = user_form
            if 'picture' in request.FILES:
                custom_form.picture = request.FILES['picture']
            custom_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect (reverse ('reuse:profile'))

    else:
        form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)

    context_dict ['form'] = form
    context_dict['profile_form'] = profile_form
    return render(request, 'reuse/edit_profile.html', context_dict)

"""
Become a seller views
"""

@login_required
def become_a_seller(request, user_name_slug):
    
    context_dict = {'title': 'Join the team'}
    
    user = request.user
    context_dict['username'] = user.username
    profile = UserProfile.objects.get(user=user)
    context_dict['profile'] = profile
    
    if request.method == 'POST':
        form = SellerForm(request.POST)
        listPay = request.POST.keys()
        if 'paypal' in listPay:
            profile.paypal = True
        if 'cash' in listPay:
            profile.cash = True
        if 'bank_transfer' in listPay:
            profile.bank_transfer = True
        
        profile.isSeller = True
        profile.save()
        return render(request, 'reuse/become_a_seller.html', context_dict)
    
    form = SellerForm()
    context_dict['form'] = form
    return render(request, 'reuse/become_a_seller.html', context_dict)

def seller_manual(request):
    context_dict = {}
    context_dict['title'] = 'The Seller Manual'
    return render(request, 'reuse/seller_manual.html', context_dict)
    

"""
User Profile view
"""

@login_required  
def view_profile(request, user_name_slug):
    #Need this for the mega menu at the nav bar --> No longer, fixed with template tags <3
    owned = False
    context_dict = {}

    profile = UserProfile.objects.get(slug=user_name_slug)
    if request.user == profile.user:
        owned = True
        
    context_dict['address'] = profile.address
    context_dict['city'] = profile.city
    context_dict['postcode'] = profile.postcode
    context_dict['description'] = profile.description
    context_dict['picture'] = profile.picture
    context_dict['isSeller'] = profile.isSeller
    context_dict['owned'] = owned
    if profile.isSeller:
        try:
            products = CurrentProduct.objects.filter(seller=profile).order_by('date')
        except CurrentProduct.DoesNotExist:
            products = None
        context_dict['products'] = products

    return render(request, 'reuse/profile.html', context_dict)
    

"""
Login view 
"""
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print(user)
        if user:
            if user.is_active:
                login(request, user)
                return redirect (reverse ('reuse:homepage'))
            else:
                return HttpResponse("Your account is disabled")
        else:
            print(f"Invalid login details:{username}, {password}")
            return HttpResponse ("Invalid login details supplied.")
    else:
        return render(request, 'reuse/login.html')
        
@login_required
def user_logout(request):
     logout(request)
     return redirect(reverse('reuse:homepage'))

@login_required
def change_password(request, user_name_slug):
    
    context_dict = {}
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Your password has been updated successfully!')
            return redirect('reuse:homepage')
        else:
            messages.error(request, 'Please correct the error(s) below.')
    else:
        form = PasswordChangeForm(request.user)
    context_dict['form']=form
    return render(request, 'reuse/change_password.html',ccontext_dict)


def current_products(request, user_name_slug):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    try:
        currentProducts = CurrentProduct.objects.filter(seller=profile)
    except CurrentProduct.DoesNotExist:
        currentProducts = None
    
    context_dict = {}
    context_dict['user'] = user
    context_dict['profile'] = profile
    context_dict['products'] = currentProducts
    return render(request, 'reuse/current_products.html', context_dict)


def sold_products(request, user_name_slug):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    try:
        soldProducts = SoldProduct.objects.filter(seller=profile)
    except SoldProduct.DoesNotExist:
        soldProducts = None
    
    context_dict = {}
    context_dict['user'] = user
    context_dict['profile'] = profile
    context_dict['products'] = soldProducts
    print(context_dict)
    return render(request, 'reuse/sold_products.html', context_dict)

def past_orders(request, user_name_slug):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    try:
        soldProducts = SoldProduct.objects.filter(buyer=profile)
    except SoldProduct.DoesNotExist:
        soldProducts = None
    context_dict = {}
    context_dict['user'] = user
    context_dict['profile'] = profile
    context_dict['products'] = soldProducts
    return render(request, 'reuse/past_orders.html', context_dict)
    

def show_category(request, category_name_slug):
     context_dict = {}
     try:
         category = Category.objects.get(slug=category_name_slug)
         subCat = Subcategory.objects.filter(category=category)
         context_dict['subcategories'] = subCat
         context_dict['category'] = category
     except Category.DoesNotExist:
         context_dict['subcategories'] = None
         context_dict['category'] = None
    
     return render(request, 'reuse/category.html', context=context_dict)

def show_sub(request, category_name_slug, subcategory_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        
    try:
        subcategory = Subcategory.objects.get(slug=subcategory_name_slug)
        products = CurrentProduct.objects.filter(subcategory=subcategory)
        context_dict['subcategory'] = subcategory
        context_dict['products'] = products
        context_dict['user'] = request.user
        context_dict['profile'] = UserProfile.objects.get(user=context_dict['user'])
    except Subcategory.DoesNotExist:
        context_dict['subcategory'] = None
        context_dict['products'] = None
    return render(request,'reuse/subcategory.html',context=context_dict)
    
def show_product(request, category_name_slug, subcategory_name_slug, product_name_slug):
    context_dict = {}
    try:
        category = get_object_or_404(Category,slug=category_name_slug)
        subcategory = get_object_or_404(Subcategory,slug=subcategory_name_slug)
        product = CurrentProduct.objects.get(slug=product_name_slug)
        context_dict['user'] = request.user
        context_dict['profile'] = UserProfile.objects.get(user=context_dict['user'])
        context_dict['subcategory'] = subcategory
        context_dict['category'] = category
        context_dict['product'] = product
    except CurrentProduct.DoesNotExist:
        context_dict['subcategory'] = None
        context_dict['category'] = None
        context_dict['product'] = None
    return render(request,'reuse/product.html',context=context_dict)

"""
Successful login with Google Account
"""
def manage(request):
    return render(request, 'reuse/manage.html')


def wishlist(request, user_name_slug):
    user = request.user.id
    try:
        userProfile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        print("you don't have a userprofile")
        return redirect('/reuse/')
    
    try:
        wishlist = Wishlist.objects.get(user=userProfile)
        products = wishlist.products.all()
    except Wishlist.DoesNotExist:
        return redirect('/reuse/')
    
    return render(request,'reuse/wishlist.html', {'products': products})


def get_shop_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = product_posts.objects.filter(
                Q(title_icontains=q),
                Q(body_icontains=q)
            ).distinct()
        
        for post in posts:
            queryset.append(post)
            
    return list(set(queryset))




@login_required
@user_is_seller
def add_product(request, category_name_slug, subcategory_name_slug):
    added = False
    try:
        subcategory = Subcategory.objects.get(slug=subcategory_name_slug)
    except Subcategory.DoesNotExist:
        subcategory = None
        
    if subcategory is None:
        return redirect('/reuse/')
        
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    
    if category is None:
        return redirect('/reuse/')
     
    form = ProductForm()
    
    user = request.user.id
    try:
        seller = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        print("you don't have a userprofile")
        return redirect('/reuse/')
    
    if request.method =='POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            if subcategory:
                product = form.save(commit=False)
                product.subcategory = subcategory
                product.category = category
                product.seller = seller
                product.save()
                added = True
                return render(request, 'reuse/add_product.html', {'form':form, 'subcategory':subcategory, 'category':category, 'product':product, 'added':added})
        else:
            print(form.errors)
    
    return render(request, 'reuse/add_product.html', {'form':form, 'subcategory':subcategory, 'category':category, 'added':added})
    

@login_required
def add_to_wishlist(request, category_name_slug, subcategory_name_slug, product_name_slug):
    try:
       category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
       category = None
       
    try:
       subcategory = Subcategory.objects.get(slug=subcategory_name_slug)
    except Subcategory.DoesNotExist:
       subcategory = None
    
    try:
       product = CurrentProduct.objects.get(slug=product_name_slug)
    except CurrentProduct.DoesNotExist:
       product = None
       
    if product is None:
       return redirect('/reuse/')
       
    user = request.user.id
    try:
        buyer = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        print("you don't have a userprofile")
        return redirect(reverse('reuse:product', kwargs={'category_name_slug':category_name_slug, 'subcategory_name_slug':subcategory_name_slug, 'product_name_slug':product_name_slug}))
        
    try:
        wishlist = Wishlist.objects.get(user=buyer)
    except Wishlist.DoesNotExist:
        print("Can't find your wishlist")
        return redirect(reverse('reuse:product', kwargs={'category_name_slug':category_name_slug, 'subcategory_name_slug':subcategory_name_slug, 'product_name_slug':product_name_slug}))
    
    if request.method == 'POST':
        if product:
            wishlist.products.add(product)
            wishlist.save()
            # Change to pop up
            return redirect(reverse('reuse:product', kwargs={'category_name_slug':category_name_slug, 'subcategory_name_slug':subcategory_name_slug, 'product_name_slug':product_name_slug}))
    
    return render(request, 'reuse/product.html', {'category': category, 'subcategory': subcategory, 'product': product})
            
