# from django.contrib.auth import views as auth_views
from django.urls import path
from .import views


urlpatterns = [

    path('', views.home, name='home'),
    path('products',views.products, name='products'),
    path('create',views.create, name='create'),
     path('update/<int:id>/',views.updateProd, name='update'),
    path('details/<int:id>/', views.Prod_detail,name='details'),
    path('delete_product/<str:pk>/', views.deleteProduct,name='delete_product'),


    path('login',views.loginPage, name='login'),
    path('logout',views.logoutUser, name='logout'),
    path('register',views.registerPage, name='register'),


    path('add_tocart', views.Add_tocart,name='add_tocart'),
    path('cart', views.cart_total,name='cart'),
       

    path('create_address/', views.create_address,name='create_address'),
    # path('cust_address/', views.cust_address,name='cust_address'),
    path('update_address/<str:pk>/', views.update_address,name='update_address'),
    path('delete_address/<str:pk>/', views.delete_address,name='delete_address'),

    path('customer_info/',views.customer_info,name='customer_info'),
    # path('customer/<str:pk_test>/',views.customer,name='customer'),

    # path('create_order/<int:id>/', views.createOrder,name='create_order'),
    # path('update_order/<str:pk>/', views.updateOrder,name='update_order'),
    # path('delete_order/<str:pk>/', views.deleteOrder,name='delete_order'),

    path('profile', views.profile,name='profile'),
    # path('profile_settings', views.profile_settings,name='profile_settings'),

        path('orders/', views.order_cust,name='orders'),
        path('create_order/', views.create_order,name='create_order'),

    # path('pay_order', views.pay_order,name='pay_order'),
    

]