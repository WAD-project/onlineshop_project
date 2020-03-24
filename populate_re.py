import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlineshop_project.settings')

import django
django.setup()
from reuse.models import Category, Subcategory, CurrentProduct, SoldProduct, UserProfile, Review

def populate():

    booksSubcat = [
        {'name': 'Sci Fi'},
        {'name': 'Art'},
        {'name': 'Romance'},
        {'name': 'Action'},
        {'name': 'Comics'},
        {'name': 'Classics'},
        {'name': 'Drama'},
        {'name': 'Biographies'},
        {'name': 'Poetry'}]
        
    clothesSubcat = [
        {'name': 'Skirts'},
        {'name': 'Shirts'},
        {'name': 'Trousers'},
        {'name': 'Dresses'},
        {'name': 'Blouses'}]
        
    otherSubcat = [
        {'name': 'Kid Toys'},
        {'name': 'Kitchen Utelsils'},
        {'name': 'Stationary'},
        {'name': 'Other'}]
        
    categories = {'Books': {'subcategories': booksSubcat},
       'Clothes': {'subcategories': clothesSubcat},
       'Other': {'subcategories': otherSubcat}
    }
       
    for cat, cat_data in categories.items():
        c = add_cat(cat)
        for p in cat_data['subcategories']:
            add_subcat(c, p['name'])
            
    for c in Category.objects.all():
        for p in Subcategory.objects.filter(category=c):
            print(f'- {c}: {p}')
            
def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c
    
def add_subcat(cat, name):
    s = Subcategory.objects.get_or_create(category=cat, name=name)[0]
    s.save()
    return s

if __name__ == '__main__':
    print('Starting re population script...')
    populate()
    
