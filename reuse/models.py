from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
# YEYYY Let's build some models


# User
# address - string
# description - text
# picture - image
# DOB - date field
# is seller - boolean
# payement info?
# rating - float

class UserProfile(models.Model):
    # Take from here username, password, email, first:_name, last_name
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # this will probably change
    address = models.CharField(max_length = 128)
    city = models.CharField(max_length = 20)
    postcode = models.CharField(max_length = 10)
    description = models.TextField(help_text = "Tell us something about you")
    # create this folder and the link
    picture = models.ImageField(upload_to='profile_images', default='profile_images/default-user.png')
    dob = models.DateField(null=True)
    isSeller = models.BooleanField(default = False)
    ratings = models.FloatField(null = True)
    slug = models.SlugField(unique = True)
    paypal = models.BooleanField(default = False)
    cash = models.BooleanField(default = False)
    bank_transfer = models.BooleanField(default = False)
    date_reg = models.DateField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username
 
 
# Category
# has a name - String
# and a number of subcat - int

class Category(models.Model):
    name = models.CharField(max_length = 128, unique = True)
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
    name = models.CharField(max_length = 128, unique = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
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
# dat - date and time field to indicate when product is added to the site 
# pictures - image fields (give 'em five?)
# what about the address?

class Product(models.Model):
    name = models.CharField(max_length = 128, help_text = "Eg. Notebook")
    subcategory = models.ForeignKey(Subcategory, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete = models.CASCADE)
    description = models.TextField(help_text = "Tell the buyers something about your product")
    price = models.FloatField(default = 0, help_text = "3.50")
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    # do i need this to be unique?
    slug = models.SlugField(unique = True)
    
    image1 = models.ImageField(upload_to='product_images', default='product_images/default.png')
    
    def save(self, *args, **kwargs):
           self.slug = slugify(self.name)
           super(Product, self).save(*args, **kwargs)
        
    class Meta:
        abstract = True
        
    def __str__(self):
        return self.name

class CurrentProduct(Product):
    image2 = models.ImageField(upload_to='product_images', blank = True)
    image3 = models.ImageField(upload_to='product_images', blank = True)
    image4 = models.ImageField(upload_to='product_images', blank = True)
    image5 = models.ImageField(upload_to='product_images', blank = True)
    seller = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name="seller")
    
class SoldProduct(Product):
    buyer = models.ForeignKey(UserProfile, on_delete=models.SET("This user no longer exists"), blank = False, related_name="buyer" )
    seller = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name="sold_by")


#class Wishlist(model.Model):
#liker = models.ForeignKey(UserProfile, )

# Review
# Maker - Foreign key
# Sold - foreign key
# Text - Textfield
# Rating - int
# Title - string

class Review(models.Model):
    title = models.CharField(max_length = 128, help_text = "Insert title here")
    text = models.TextField(help_text = "Tell us how the seller was")
    product = models.OneToOneField(SoldProduct, on_delete=models.SET("This product no longer exists"))
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="reviewed")
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="reviewer")
    on_date = models.DateField(auto_now_add=True, blank=True, null=True)
    rating = models.IntegerField(blank = False)
    def __str__(self):
        return self.title
        

class Wishlist(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    #might need a fix
    products = models.ManyToManyField(CurrentProduct)




