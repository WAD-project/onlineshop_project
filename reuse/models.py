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
# buyer - foreign Key - can be null
# subcategory - foreign key
# price - float
# pictures - image fields (give 'em five?)
# what about the address?

class Product(models.Model):
    name = models.CharField(max_lenght = 128, help_text = "Eg. Notebook")
    subcategory = models.ForeignKey(Subcategory, on_delete = models.CASCADE)
    description = models.TextField(help_text = "Tell the buyers something about your product")
    seller = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    price = models.FloatField(default = 0, help_text = "3.50")
    # do i need this to be unique?
    slug = models.SlugField(unique = True)
    
    # put upload to with folder
    image1 = models.ImageField(blank = True)
    
    def save(self, *args, **kwargs):
           self.slug = slugify(self.name)
           super(Product, self).save(*args, **kwargs)
        
    class Meta:
        abstract = True
        
    def __str__(self):
        return self.name

class CurrentProduct(Product):
    # still miss the folder
    image2 = models.ImageField(blank = True)
    image3 = models.ImageField(blank = True)
    image4 = models.ImageField(blank = True)
    image5 = models.ImageField(blank = True)
    
class SoldProduct(Product):
    buyer = models.ForeignKey(UserProfile, on_delete.SET("This user no longer exists"), blank = False)
        

# User
# address - string
# description - text
# picture - image
# DOB - date field
# is seller - boolean
# payement info?
# rating - float
#

class UserProfile(models.Model):
    # Take from here username, password, email, first:_name, last_name
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # this will probably change
    streetAndNumber = CharField(max_lenght = 128, help_text = "Eg. Woodlands road 26")
    city = CharField(max_lenght = 20, help_text = "Eg. Glasgow")
    postcode = CharField(max_lenght = 10, help_text = "Eg. G4 7AL")
    description = TextField(help_text = "Tell us something about you")
    # create this folder and the link
    picture = models.ImageField(upload_to = 'profile_images', blank = True)
    dob = models.DateField()
    isSeller = BooleanField(default = False)
    ratings = FloatField(null = True)
    
    likedProducts = models.ManyToManyField(CurrentProduct, on_delete=models.CASCADE)
    cartProducts = models.ManyToManyField(CurrentProduct, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
        

# Review
# Maker - Foreign key
# Sold - foreign key
# Text - Textfield
# Rating - int
# Title - string

class Review(models.Model):
    title = models.CharField(max_lenght = 128, help_text = "Insert title here")
    text = models.TextField(help_text = "Tell us how the seller was")
    rating = models.IntegerField(blank = False)
    product = models.ForeignKey(SoldProduct, on_delete=models.SET("This product no longer exists"))
    seller = product.seller
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
        



