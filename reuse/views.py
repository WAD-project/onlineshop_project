from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from reuse.models import Category, Subcategory, Product, CurrentProduct, UserProfile
from reuse.forms import ProductForm, UserForm, UserProfileForm,  UserUpdateForm,ProfileUpdateForm
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
    #recently_added = CurrentProduct.objects.order_by('-dat')[:4]
    #context_dict["recently_added"]=recently_added
    for cat in category_list:
        context_dict['categories'][cat] = Subcategory.objects.filter(category=cat).order_by('name')
        
    response = render(request, 'reuse/homepage.html', context = context_dict)
    return response

def about(request):
    return render(request,'reuse/about.html')

def faq(request):
    return render(request, 'reuse/faq.html')
    
def contact_us(request):
    # Add stuff here
    return render(request, 'reuse/contact_us.html')
    
@login_required
def add_product(request, category_name_slug, subcategory_name_slug):
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
                # This has to change - successfully added screen
                return redirect('/reuse/')
        else:
            print(form.errors)
    
    return render(request, 'reuse/add_product.html', {'form':form, 'subcategory':subcategory, 'category':category})




def register(request):
    category_list = Category.objects.order_by('name')
    context_dict = {}
    context_dict['title'] = 'Welcome'
    context_dict['categories'] = {}
    for cat in category_list:
        context_dict['categories'][cat] = Subcategory.objects.filter(category=cat).order_by('name')
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
        else:
            print(user_form.errors, profile_form.errors)
            
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    context_dict['user_form'] = user_form
    context_dict['profile_form'] = profile_form
    context_dict['registered']=registered 
    return render(request,'reuse/register.html',
    context_dict)


"""
Edit profile view 
"""
@login_required 
def edit_profile(request):
    #This is for the mega menu at the navbar
    category_list = Category.objects.order_by('name')
    context_dict = {}
    context_dict['title'] = 'Welcome'
    context_dict['categories'] = {}
    for cat in category_list:
        context_dict['categories'][cat] = Subcategory.objects.filter(category=cat).order_by('name')

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
    context_dict['profile_form']=profile_form
    return render(request, 'reuse/edit_profile.html', context_dict)

"""
User Profile view
"""
@login_required  
def view_profile(request):
    #Need this for the mega menu at the nav bar
    category_list = Category.objects.order_by('name')
    context_dict = {}
    context_dict['title'] = 'Welcome'
    context_dict['categories'] = {}
    for cat in category_list:
        context_dict['categories'][cat] = Subcategory.objects.filter(category=cat).order_by('name')


    # for the profile
    #get user profile
    profile=request.user.userprofile
    context_dict['address'] = profile.address
    context_dict['city'] = profile.city
    context_dict['postcode'] = profile.postcode
    context_dict['description'] = profile.description
    context_dict['picture'] = profile.picture

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
def change_password(request):
    #This is for the mega menu at the navbar
    category_list = Category.objects.order_by('name')
    context_dict = {}
    context_dict['title'] = 'Welcome'
    context_dict['categories'] = {}
    for cat in category_list:
        context_dict['categories'][cat] = Subcategory.objects.filter(category=cat).order_by('name')

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Your password was successfully updated!')
            return redirect('reuse:homepage')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    context_dict['form']=form
    return render(request, 'reuse/change_password.html', 
        context_dict
    )




def show_category(request,category_name_slug):
     context_dict = {}
     try:
         category = Category.objects.get(slug=category_name_slug)
         subCat = Subcategory.objects.filter(category=category)
         context_dict['subcategories'] = subCat
         context_dict['category'] = category
     except Category.DoesNotExist:
         context_dict['subcategories'] = None
         context_dict['category'] = None
         
     return render(request,'reuse/category.html',context=context_dict)

def show_sub(request, category_name_slug, subcategory_name_slug):
    context_dict = {}
    try:
        category = get_object_or_404(Category, slug=category_name_slug)
        subcategory = Subcategory.objects.get(slug=subcategory_name_slug)
        products = CurrentProduct.objects.filter(subcategory=subcategory)
        context_dict['subcategory'] = subcategory
        context_dict['category'] = category
        context_dict['products'] = products
    except Subcategory.DoesNotExist:
        context_dict['subcategory'] = None
        context_dict['category'] = None
        context_dict['products'] = None
    return render(request,'reuse/subcategory.html',context=context_dict)
    
def show_product(request, category_name_slug, subcategory_name_slug, product_name_slug):
    context_dict = {}
    try:
        category = get_object_or_404(Category,slug=category_name_slug)
        subcategory = get_object_or_404(Subcategory,slug=subcategory_name_slug)
        product = CurrentProduct.objects.get(slug=product_name_slug)
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


def wishlist(request):
    category_list = Category.objects.order_by('name')
    context_dict = {}
    context_dict['title'] = 'Welcome'
    context_dict['categories'] = {}
    #recently_added = CurrentProduct.objects.order_by('-dat')[:4]
    for cat in category_list:
        context_dict['categories'][cat] = Subcategory.objects.filter(category=cat).order_by('name')
    return render(request,'reuse/wishlist.html',context_dict)
def shoppingcart(request):
    return render(request,'reuse/shoppingcart.html')


def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = MODEL.objects.filter(name__startswith=q)
        results = []
        print (q)
        for r in search_qs:
            results.append(r.FIELD)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


