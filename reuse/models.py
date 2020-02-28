from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
# YEYYY Let's build some models

# Category
# has a name - String
# and a number of subcat - int

class Category(models.Model):
    name = models.CharField(max_lenght = 128, unique = True)
    subcat = models.IntegerField(default = 0)
    slug = models.SlugField(unique = True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = "categories"
        
    def __str__(self):
        return self.name
        

# Subcategory
# name - String
# category - foreing key
# n products - int

class Subcategory(models.Model):
    name = models.CharField(max_lenght = 128, unique = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    products = models.IntegerField(default = 0)
    slug = models.SlugField(unique = True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subcategory, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = "subcategories"
        
    def __str__(self):
        return self.name


# Product
# name - String
# description - text
# seller - foreign Key
# current - boolean - so actually int (0 false 1 true)
# buyer - foreign Key - can be null
# subcategory - foreign key
# price - float
# pictures - image fields (give 'em five?)
# what about the address?

class Product(models.Model):
    name = models.CharField(max_lenght = 128, unique = True)
    subcategory = models.ForeignKey(Subcategory, on_delete = models.CASCADE)
    description = models.TextField()
    current = models.BooleanField(default = True)
    seller = models.ForeignKey(Seller, on_delete = models.CASCADE)
    buyer = models.ForeignKey(Buyer, to_field = "email", on_delete.SET("This user no longer exists"), null = True)
    price = models.FloatField(default = 0)
    slug = models.SlugField(unique = True)
    
    # put upload to with folder
    image1 = models.ImageField(blank = True)
    image2 = models.ImageField(blank = True)
    image3 = models.ImageField(blank = True)
    image4 = models.ImageField(blank = True)
    image5 = models.ImageField(blank = True)
    
    def save(self, *args, **kwargs):
           self.slug = slugify(self.name)
           super(Product, self).save(*args, **kwargs)
           
    def __str__(self):
        return self.name


# User
# Email - email
# name - String
# surname - string
# username - string
# address - string
# description - text
# picture - image
# DOB - date field
# is seller - boolean
# password --> User deals with it
# payement info?
# rating - float
#

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    email = models.EmailField(unique = True)
    name = CharField(max_lenght = 20)
    surname = CharField(max_lenght = 20)
    username = CharField(max_lenght = 20, unique = True)
    # this will probably change
    address = CharField(max_lenght = 128)
    description = TextField()
    #create this folder and the link
    picture = models.ImageField(upload_to = 'profile_images', blank = True)
    dob = models.DateField()
    isSeller = BooleanField(default = False)
    ratings = FloatField(null = True)
    
    # I am a bit stuck on making all the relationships
    # I'll try again later or tomorrow
    
    def __str__(self):
        return self.user.username
        


