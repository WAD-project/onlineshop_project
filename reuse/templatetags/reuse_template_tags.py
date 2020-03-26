from django import template
from reuse.models import Category, Subcategory, UserProfile

register = template.Library()

@register.inclusion_tag('reuse/categories.html')
def get_category_list():
    catlist = {}
    category_list = Category.objects.order_by('name')
    catlist['categories'] = {}
    
    for cat in category_list:
        catlist['categories'][cat] = Subcategory.objects.filter(category=cat).order_by('name')
    
    return catlist

@register.simple_tag
def get_user_name(user):
    try:
        profile = UserProfile.objects.get(user=user)
        name = profile.slug
    except:
        name = None
    return name
