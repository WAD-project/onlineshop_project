from django import forms
from reuse.models import Product, UserProfile
from django.contrib.auth.models import User


class ProductForm (forms.ModelForm):
    name = forms.CharField(max_length = 128, help_text="Please enter the name of the product.")
    description = forms.CharField(help_text="Enter short description of the product.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    price=forms.FloatField(help_text="Price of the product.", min_value=0)
    class Meta:
        model=Product
        exclude=('subcategory',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',)
        
class UserProfileForm(forms.ModelForm):
    #slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = UserProfile
        #add other fields
        fields = ('picture',)


