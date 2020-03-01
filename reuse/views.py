from django.shortcuts import render
from django.http import HttpResponse
from reuse.models import Category, Subcategory

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
