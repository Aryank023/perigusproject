"""finalproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path 
from ecommerceapp import views
from django.conf import settings
from django.conf.urls.static import static
from ecommerceapp.views  import userviewproduct,detailproduct

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vendorlogin',views.vendorlogin,name='vendorlogin'),
    path('vendorregister',views.vendorregister,name='vendorregister'),
    path('userlogin',views.userlogin,name='userlogin'),
    path('userregister',views.userregister,name='useregister'),
    path('vendordashboard',views.vendordashboard,name='vendordashboard'),


    

    path('vendorprofile',views.vendorprofile,name='vendorprofile'),
    path('userprofile',views.userprofile,name='userprofile'),

    path('vendoreditprofile',views.vendoreditprofile,name='vendoreditprofile'),
    path('usereditprofile',views.usereditprofile,name='usereditprofile'),


    path('addproduct',views.addproduct,name='addproduct'),
    path('viewproduct',views.viewproduct,name='viewproduct'),
    
    # path('deleteproduct/<int:pk>',deleteproduct.as_view(),name='deleteproduct'),
    path('deleteproduct/<int:pk>',views.delete_product,name='deleteproduct'),
    path('editproduct/<int:pk>',views.editproduct,name='editproduct'),


    path('vendorlogout',views.vendorlogout,name='vendorlogout'),
    path('userlogout',views.userlogout,name='userlogout'),


    path('userviewproduct',userviewproduct.as_view(),name='userviewproduct'),
    path('usersearchproduct',views.usersearchproduct,name='usersearchproduct'),
    path('addtocart',views.addtocart,name='addtocart'),
    path('viewcart',views.viewcart,name='viewcart'),
    path('changequantity',views.changequantity,name='changequantity'),


    path('detailviewproduct/<int:pk>', detailproduct.as_view(), name='detailviewproduct'),


    path('displayjeans',views.jeansdisplay,name='displayjeans'),
    path('displayshirt',views.shirtdisplay,name='displayshirt'),
    path('displaytshirt',views.tshirtdisplay,name='displaytshirt'),
    path('displayhoodie',views.hoodiedisplay,name='displayhoodie'),
    path('displayskirt',views.skirtdisplay,name='displayskirt'),
    path('displaysweatshirt',views.displaysweatshirt,name='displaysweatshirt'),
    path('displayjacket',views.displayjacket,name='displayjacket'),
    path('displaytrouser',views.displaytrouser,name='displaytrouser'),
    path('displaytop',views.displaytop,name='displaytop'),
    path('displaydress',views.displaydress,name='displaydress'),
    path('displaysweater',views.displaysweater,name='displaysweater'),
    path('displayshorts',views.displayshorts,name='displayshorts'),


    path('summary',views.summary,name='summary'),
    path('placeorder',views.placeorder,name='placeorder'),
    path('paymentsuccess',views.paymentsuccess,name='paymentsuccess'),
    path('homepage',views.homepage,name='homepage'),

    path('subscription-plans/', views.subscription_plans, name='subscription_plans'),
    path('subscription_plans/<int:subscription_id>/', views.subscription_plans, name='subscription_plans'),
    path('vendor-subscriptions/', views.vendor_subscriptions, name='vendor_subscriptions'),
    
    
    # path('add_to_cart/<int:subscription_id>/', views.add_to_cart, name='add_to_cart'),
    # path('view_cart/', views.view_cart, name='view_cart'),
    # path('vendorsummary/', views.vendorsummary, name='vendorsummary'),
    # path('place_order/', views.place_order, name='place_order'),
    path('payment_success', views.payment_success, name='payment_success'),
    path('purchase-subscription/<int:subscription_id>/', views.purchase_subscription, name='purchase_subscription'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)