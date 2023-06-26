from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields ='__all__'
        
class CustomerForm(ModelForm):
    class Meta:
        model=Customer
        fields='__all__'
        exclude=['user','password']

class CustomerAddressForm(ModelForm):
    class Meta:
        model = CustomerAddress
        fields ='__all__'
    # def __str__(self, user=None, *args, **kwargs): # note the additional user param
    #   self.customer = CustomerAddress.objects.filter(customer=user)
    #   super(CustomerAddressForm, self).__init__(*args, **kwargs)
    #   self.fields['customer'].queryset = self.customer
 
        
class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class OrderForm(ModelForm):
    class Meta:
        model=Order
        fields='__all__'
        exclude=['product']