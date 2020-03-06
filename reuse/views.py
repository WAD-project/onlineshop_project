from django.shortcuts import render, redirect
from django.http import HttpResponse
from reuse.models import Category, Subcategory
from reuse.forms import ProductForm, UserForm, UserProfileForm



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


def register (request):
    registered=False
    if request.method=='POST':
        user_form=UserForm(request.POST)
        profile_form=UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            if 'picture' in request.FILES:
                profile.picture=request.FILES['picture']
            profile.save()
            registered=True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form=UserForm()
        profile_form=UserProfileForm()
    return render(request, 'reuse/register.html', context = {'user_form': user_form,  'profile_form': profile_form,  'registered': registered})

def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username, password=password)
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

