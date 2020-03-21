from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from reuse.models import Category, Subcategory, Product, CurrentProduct, UserProfile
from reuse.forms import ProductForm, UserForm, UserProfileForm, ProfileForm, UserUpdateForm,ProfileUpdateForm
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
        
    return render(request,'reuse/register.html',
    context = {'user_form': user_form,'profile_form': profile_form,
    'registered': registered})


"""
Edit profile view 
"""
@login_required 
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            messages.success(request, f'Your account has been updated!')
            return redirect (reverse ('reuse:homepage'))

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user)

    context = {
        'form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'reuse/edit_profile.html', context)

"""
User Profile view
"""
@login_required  
def view_profile(request):
    return render(request, 'reuse/profile.html')

"""
Login view 
"""
def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
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
    return render(request, 'reuse/change_password.html', {
        'form': form
    })




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
    return render(request,'reuse/wishlist.html')
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


