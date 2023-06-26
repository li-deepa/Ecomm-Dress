from uuid import uuid4
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
import os
# Create your models here.

class Product(models.Model):
    product_name=models.CharField(max_length=200,null=True)
    image= models.ImageField(null=True,blank=True)
    description=models.CharField(max_length=200,null=True,blank=True)
    price=models.FloatField(null=True)

    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url
        
    def __str__(self) -> str:
        return self.product_name

    def get_absolute_url(self):
        return reverse("details",kwargs={"id":self.id})#f"/products/{self.id}"

    @property
    def relative_path(self):
        return os.path.relpath(self.path, settings.MEDIA_ROOT)
    

class Cart(models.Model):
    id=models.UUIDField(default=uuid.uuid4,primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    completed=models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
    
    @property   
    def total_price(self):
        cartItems=self.cartItems.all()
        total=sum([item.product.price *item.quantity for item in cartItems])
        return total
        
    @property
    def num_of_items(self):
        cartItems=self.cartItems.all()
        quantity=sum([item.quantity for item in cartItems])
        return quantity
    
    @property
    def tax_items(self):
        cartItems=self.cartItems.all()
        total=round(sum([item.product.price *item.quantity for item in cartItems])*0.20,2)
        return total
    @property
    def total_afterTax(self):
        cartItems=self.cartItems.all()
        total=self.tax_items+self.total_price
        return total

class CartItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='items')
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cartItems')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product.product_name

    @property   
    def item_price(self):
        new_price=self.product.price*self.quantity
        return new_price
    
    


class Customer(models.Model):
    user= models.OneToOneField(User,related_name = "customer",null=True,blank=True,on_delete=models.CASCADE)
    name= models.CharField(max_length=200,null=True)
    email= models.CharField(max_length=200,null=True)
    phone=models.CharField(max_length=200,null=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    password=models.CharField(max_length=9,null=True)
    #name=models.CharField(max_length=200)


    def __str__(self):
        return self.name
    
    
       

class CustomerAddress(models.Model):
    customer=models.ForeignKey(Customer,related_name = "shippingAddress",on_delete=models.SET_NULL,null=True)
    street_address=models.CharField(max_length=200,null=False)
    city=models.CharField(max_length=200,null=False)
    state=models.CharField(max_length=200,null=False)
    zipcode=models.CharField(max_length=200,null=False)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.street_address
    
    def get_absolute_url(self):
        return reverse("update_address",kwargs={"pk":self.id})#f"/products/{self.id}"

   

class Order(models.Model):
    STATUS=(
        ('pending','pending'),
        ('out for delivery','out for delivery'),
        ('delivered','delivered')
    )
    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    ship_address=models.ForeignKey(CustomerAddress,related_name='ship_address',null=True,on_delete=models.SET_NULL)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    status=models.CharField(max_length=200,null=True,choices=STATUS)
    transaction_id=models.CharField(max_length=200,null=True)

    


    def __str__(self) -> str:
        return  str(self.id)

    