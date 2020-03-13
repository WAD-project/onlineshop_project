from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from reuse.models import Category, Subcategory,Product
from reuse.forms import ProductForm, UserForm, UserProfileForm, EditProfileForm, ProfileForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse




# Create your views here.

def homepage(request):
    category_list = Category.objects.order_by('name')
    context_dict = {}
    context_dict['title'] = 'Welcome'
    context_dict['categories'] = {}
    
    for cat in category_list:
        context_dict['categories'][cat] = Subcategory.objects.filter(category=cat).order_by('name')
        
    response = render(request, 'reuse/homepage.html', context = context_dict)
    return response

def about(request):
    return render(request,'reuse/about.html')
#@login_required
def add_product(request):
    form=ProductForm()
    if request.method =='POST':
        form=ProductForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect ('/reuse/')
        else:
            print (form.errors)
    return render(request, 'reuse/add_product.html',{'form':form})
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

@login_required
def edit_profile(request):
    if request.method =='POST':
        user_form=EditProfileForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.save()
            profile = profile_form.save(commit=False)
            profile.user=user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            profile.save()
        else:
             print(user_form.errors, profile_form.errors)
    else:
        user_form = EditProfileForm()
        profile_form = ProfileForm()
    return render(request, 'reuse/edit_profile.html', context={'form': user_form, 'profile_form':profile_form})




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
         subCat=Subcategory.objects.filter(category=category)

         context_dict['subcategories'] = subCat
         context_dict['category'] = category
     except Category.DoesNotExist:
         context_dict['subcategories'] = None
         context_dict['category'] = None
     return render(request,'reuse/category.html',context=context_dict)

def show_sub(request,category_name_slug,subcategory_name_slug):
    context_dict = {}
    category=get_object_or_404(Category,slug=category_name_slug)
    subcategory=get_object_or_404(Subcategory,slug=subcategory_name_slug)
    context_dict['subcategory'] = subcategory
    context_dict['categories'] = category
    return render(request,'reuse/subcategory.html',context=context_dict)
def show_product(request,category_name_slug,subcategory_name_slug,product_name_slug):
    context_dict = {}
    category=get_object_or_404(Category,slug=category_name_slug)
    subcategory=get_object_or_404(Subcategory,slug=subcategory_name_slug)
    product=get_object_or_404(Product,slug=product_name_slug)
    context_dict['subcategory'] = subcategory
    context_dict['categories'] = category
    context_dict['product'] = product
    return render(request,'reuse/product.html',context=context_dict)
def manage(request):
    return render(request, 'reuse/manage.html')
def wishlist(request):
    return render(request,'reuse/wishlist.html')
def shoppingcart(request):
    return render(request,'reuse/shoppingcart.html')



