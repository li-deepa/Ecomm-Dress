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

def profile_settings(request):
    customer=request.user.customer
    form=CustomerForm(instance=customer)
    if request.method =='POST':
        form=CustomerForm(request.POST,instance=customer)
        if form.is_valid()  :
            form.save()
            return redirect('cust_address')
    context={'form':form,'customer':customer}
    return render(request,"ecomm/profile_settings.html",context)

def createOrder(request,pk):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=5)
    # customer=Customer.objects.get(id=pk)
    # form=OrderForm(initial={'customer':customer})
    cart=None
    cartItems=[]
    customer=Customer.objects.all()
    cart,created=Cart.objects.get_or_create(user=request.user,completed=False)
    

    cartItems=cart.cartItems.all()
    formset=OrderFormSet(queryset=Order.objects.none(),instance=cartItems)
    if request.method=='POST':
        # form=OrderForm(request.POST)
        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('profile')
    context={'formset':formset,'cart':cart,'cartItems':cartItems}
    return render(request,"ecomm/order_form.html",context)

def customer(request,pk_test):
    customer=Customer.objects.get(id=pk_test)

    orders=customer.order_set.all()
    order_count=orders.count()
    
    myFilter=OrderFilter(request.GET,queryset=orders)
    orders=myFilter.qs

    context={'customer':customer,'orders':orders,'order_count':order_count,'myFilter':myFilter}
    return render(request,'ecomm/customers.html',context)

def cust_address(request):
    customer=request.user.customer
    cu_address=CustomerAddress.objects.all()
    context={'cu_address':cu_address}
    print("show_address")
    return render(request,"ecomm/customer_address.html",context)

def updateOrder(request,id):
    order=Order.objects.get(id=id)
    form=OrderForm(instance=order)

    if request.method =='POST':
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('profile')

    context={'form':form}
    return render(request,"ecomm/updateorders.html",context)

def deleteOrder(request,pk):
        order=Order.objects.get(id=pk)
        if request.method =='POST':
            order.delete()
            return redirect('profile')
        context={'item':order}
        return render(request,"ecomm/delete_product.html",context)

def pay_order(request):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=5)
    # customer=Customer.objects.get(id=pk)
    # form=OrderForm(initial={'customer':customer})
    
    cart=None
    cartItems=[]
    customer=request.user.customer
    cart,created=Cart.objects.get_or_create(user=request.user,completed=False)
    

    cartItems=cart.cartItems.all()
    formset=OrderFormSet(queryset=Cart.objects.none(),instance=cartItems)
    if request.method=='POST':
        # form=OrderForm(request.POST)
        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('profile')
    context={'formset':formset,'cart':cart,'cartItems':cartItems}
    return render(request,"ecomm/order_form.html",context)
