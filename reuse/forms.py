from django import forms
from reuse.models import Product, UserProfile
from django.contrib.auth.models import User
import re


EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

#Add product - not finished
class ProductForm (forms.ModelForm):
    name = forms.CharField(max_length = 128, help_text="Please enter the name of the product.")
    description = forms.CharField(help_text="Enter short description of the product.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    price=forms.FloatField(help_text="Price of the product.", min_value=0)
    class Meta:
        model=Product
        exclude=('subcategory',)


class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    password2=forms.CharField(widget=forms.PasswordInput())

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not re.match(EMAIL_REGEX, email):
            raise forms.ValidationError('Invalid email format')
        return email

    class Meta:
        model = User
        fields = ('first_name', 'last_name','username','email','password',)




class UserProfileForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = UserProfile
        fields = ('picture',)

"""
#Registration
class UserForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        min_length = 6,
        max_length = 20
    )   

    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(),
        help_text="Enter the same password as before, for verification.",
        min_length = 6,
        max_length = 20
    )

    


   



"""




