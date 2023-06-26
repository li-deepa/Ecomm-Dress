import datetime
import json
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import *
from .filters import OrderFilter
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import pdfkit


# Create your views here.

def registerPage(request):
    
    form=CreateUserForm()

    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            customer=Customer.objects.create(user=user, name=user.username, email=user.email)
            # ship_address=CustomerAddress.objects.create(customer=customer)

            # print(ship_address.customer.name)
            messages.success(request,'account was created for'+username)
            return redirect('login')
    context={'form':form,}
    return render(request,'ecomm/register.html',context)

def loginPage(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
             login(request, user)
        return redirect('home')
        
        
    return render(request,'ecomm/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

def home(request):
    product=Product.objects.all()
    # if request.user.is_authenticated:
    # cart,created=Cart.objects.get_or_create(user=request.user,completed=False)
    context={'product':product,}
    return render(request,"ecomm/index.html",context)




def create(request):
    form=CreateProductForm()
    if request.method=='POST':
        form=CreateProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("products")
    context={'form':form,}
    return render(request,'ecomm/createProd.html',context)

def updateProd(request,id):
    product=Product.objects.get(id=id)
    form=CreateProductForm(instance=product)

    if request.method =='POST':
        form=CreateProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    context={'form':form}
    return render(request,'ecomm/createProd.html',context)

def deleteProduct(request,pk):
    product=Product.objects.get(id=pk)
    if request.method =='POST':
        product.delete()
        return redirect('products')
    context={'item':product}
    return render(request,"ecomm/delete_product.html",context)

def products(request):
    product=Product.objects.all()
    if request.user.is_authenticated:
         cart,created=Cart.objects.get_or_create(user=request.user,completed=False)
    context={'product':product,'cart':cart}
    return render(request,"ecomm/products.html",context)

def Prod_detail(request,id):
    subject=Product.objects.get(id=id)
    if request.user.is_authenticated:
        cart,created=Cart.objects.get_or_create(user=request.user,completed=False)
    context={'product':subject,'cart':cart}
    return render(request,"ecomm/details.html",context)


def Add_tocart(request):
    data=json.loads(request.body)
    product_id=data['id']
    action=data['action']

    product=Product.objects.get(id=product_id)
    
    cart,created=Cart.objects.get_or_create(user=request.user,completed=False)
    cartItems,created=CartItem.objects.get_or_create(cart=cart,product=product)
    
    num_items=cart.num_of_items
    if action=='add':
        cartItems.quantity=(cartItems.quantity +1)
    if action =='remove':
        cartItems.quantity=(cartItems.quantity -1)
    cartItems.save()

    if cartItems.quantity <= 0:
        cartItems.delete()
    print(action)   
    
    return JsonResponse(num_items,safe=False)




def cart_total(request):
    cart=None
    cartItems=[]
    customer=Customer.objects.all()
    cart,created=Cart.objects.get_or_create(user=request.user,completed=False)
    cartItems=cart.cartItems.all()
    context={'cart':cart,'items':cartItems,'customer':customer}
   
    return render(request,'ecomm/cartitems.html',context)

#crud operations
# @allowed_users(allowed_roles=['admin'])
def order_cust(request):
    cart=None
    cartItems=[]
    customer=Customer.objects.all()
    cart,created=Cart.objects.get_or_create(user=request.user,completed=False)
    cartItems=cart.cartItems.all()
    form=OrderForm()
    if request.method =='POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('profile')
    print(cartItems)
    context={'cart':cart,'items':cartItems,'customer':customer,'form':form}
    
    return render(request,"ecomm/ordersc.html",context)




def customer_info(request):
    customer=request.user.customer
    ship_address=CustomerAddress.objects.filter(customer=customer)
    cart,created=Cart.objects.get_or_create(user=request.user,completed=False)

    cartItems=cart.cartItems.all()
    num_items=cart.num_of_items
    tax=cart.tax_items
   
    
    context={'customer':customer,'ship_address':ship_address,'cartItems':cartItems,
             'cart':cart,'num_items':num_items,'tax':tax,}
    return render(request,'ecomm/all_customers.html',context)




    

# @allowed_users(allowed_roles=['customer'])
def profile(request):
    customer=request.user.customer
    form=CustomerForm(instance=customer)
    if request.method =='POST':
        form=CustomerForm(request.POST,instance=customer)
        if form.is_valid()  :
            form.save()
            # return redirect('cust_address')
    orders=request.user.customer.order_set.all()
    total_orders=orders.count()
    delivered=orders.filter(status='delivered').count()
    pending=orders.filter(status='pending').count()
    out_delivery=orders.filter(status='out for delivery').count()
    sh_address=CustomerAddress.objects.all()
    context={'orders':orders,'total_orders':total_orders,
    "delivered":delivered,"pending":pending,
    'out_delivery':out_delivery,'ship_address':sh_address,'form':form,'customer':customer}
    return render(request,"ecomm/profile.html",context)

    #    <a class="btn btn-md btn-outline-success" href="{% url 'profile_settings' %}">settings</a> 


def create_address(request):
    customer=request.user.customer   
    cu_address=CustomerAddress.objects.all()
    ship_address=CustomerAddress.objects.create(customer=customer)
    form=CustomerAddressForm(instance=ship_address)
    if request.method =='POST':
        form=CustomerAddressForm(request.POST,instance=ship_address)
        if form.is_valid():
            form.save()
            return redirect('profile')
    context={'form':form,'customer':customer,'cu_address':cu_address,'ship_address':ship_address}
    print("cu_address")
    print(ship_address)
    return render(request,"ecomm/customers_add.html",context)



def update_address(request,pk):
    customer=request.user.customer   
    cu_address=CustomerAddress.objects.all()
    ship_address=CustomerAddress.objects.get(id=pk)
    form=CustomerAddressForm(instance=ship_address)
    if request.method =='POST':
        form=CustomerAddressForm(request.POST,instance=ship_address)
        if  form.is_valid():
            form.save()
            return redirect('profile')
    context={'form':form,'cu_address':cu_address,'customer':customer,'ship_address':ship_address}
    return render(request,"ecomm/update_address.html",context)


def delete_address(request,pk):
    customer=request.user.customer
    cu_address=CustomerAddress.objects.all()
    ship_address=CustomerAddress.objects.get(id=pk)
    if request.method =='POST':
        ship_address.delete()
        return redirect('profile')
    context={'ship_address':ship_address,'customer':customer,'cu_address':cu_address}
    return render(request,"ecomm/delete_address.html",context)


def create_order(request):
   
    customer=request.user.customer
    cart,created=Cart.objects.get_or_create(user=request.user,completed=False)
    orders=request.user.customer.order_set.all()
    ship_address=CustomerAddress.objects.get(customer=customer)
    transaction_id=datetime.datetime.now().timestamp()

    order=Order.objects.create(customer=request.user.customer,transaction_id=transaction_id,ship_address=ship_address)
    form=OrderForm(instance=order)
   
    if request.method =='POST':
        form=OrderForm(request.POST,instance=order)
        if  form.is_valid():
            form.save()
            # return redirect('home')
    context={'form':form,'cart':cart,'orders':orders,
    'order':order,
    'ship_address':ship_address}


    return render(request,'ecomm/update_orders.html',context)
