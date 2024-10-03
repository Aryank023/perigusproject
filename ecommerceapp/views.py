from django.shortcuts import redirect, render,get_object_or_404
from django.urls import reverse, reverse_lazy
from .models import user,vendor,product,cart,category,subcategory,order,orderdetail,payment,Subscription,VendorSubscriptions,vendorpayment
from django.contrib.auth.hashers import make_password,check_password
from django.http import HttpResponse
from django.db.models import Q
from django.views.generic import ListView, DeleteView, UpdateView, DetailView, CreateView
import razorpay
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import date,datetime,timedelta
from dateutil.relativedelta import relativedelta



# Create your views here.



def vendorregister(request):
    if request.method=="GET":
        return render(request,'vendorregister.html')
    elif request.method=="POST":
        name=request.POST.get('fullname')
        age=request.POST.get('age')
        gender=request.POST.get('gender')
        phoneno=request.POST.get('phoneno')
        address=request.POST.get('address')
        state=request.POST.get('state')
        district=request.POST.get('district')
        pincode=request.POST.get('pincode')
        email=request.POST.get('email')
        password=request.POST.get('password')
        epassword= make_password(password)
        vendorobj=vendor(name=name,age=age,gender=gender,phoneno=phoneno,address=address,state=state,district=district,pincode=pincode,email=email,password=epassword)
        cust=vendor.objects.filter(email=vendorobj.email)
        if cust:
            vendorobj=vendor.objects.get(email=vendorobj.email)
            return render(request,'vendorregister.html',{'msg':'Email already exists'})
        
        vendorobj.save()
        return redirect('../vendorlogin')
    


def vendorlogin(request):
        if request.method == 'GET':
            return render(request,'vendorlogin.html')
        elif request.method == 'POST':
            useremail=request.POST.get('useremail')
            passwordd=request.POST.get('passs')

            vendorr=vendor.objects.filter(email=useremail)
            if vendorr:
                vendorobj=vendor.objects.get(email=useremail)
                flag=check_password(passwordd,vendorobj.password)

                if flag:
                    request.session['sessionvaluevendor']=vendorobj.email
                    return redirect('../vendorprofile') 
                else:
                    return render(request,'vendorlogin.html',{'msg':'incorrect username and password'})
                
            else:
                return render(request,'vendorlogin.html',{'msg':'incorrect username and password'})

def userregister(request):
    if request.method=="GET":
        return render(request,'userregister.html')
    elif request.method=="POST":
        name=request.POST.get('fullname')
        age=request.POST.get('age')
        gender=request.POST.get('gender')
        phoneno=request.POST.get('phoneno')
        address=request.POST.get('address')
        state=request.POST.get('state')
        district=request.POST.get('district')
        pincode=request.POST.get('pincode')
        email=request.POST.get('email')
        password=request.POST.get('password')
        epassword= make_password(password)
        userobj=user(name=name,age=age,gender=gender,phoneno=phoneno,address=address,state=state,district=district,pincode=pincode,email=email,password=epassword)
        cust=user.objects.filter(email=userobj.email)
        if cust:
            userobj=user.objects.get(email=userobj.email)
            return render(request,'userregister.html',{'msg':'Email already exists'})
        userobj.save()
        return redirect('../userlogin')
    

def userlogin(request):
        if request.method == 'GET':
            return render(request,'userlogin.html')
        elif request.method == 'POST':
            useremail=request.POST.get('useremail')
            passwordd=request.POST.get('passs')

            userr=user.objects.filter(email=useremail)
            if userr:
                userobj=user.objects.get(email=useremail)
                flag=check_password(passwordd,userobj.password)

                if flag:
                    request.session['sessionvalue']=userobj.email
                    return render(request,'homepage.html',{'session':request.session['sessionvalue']})
                else:
                    return render(request,'userlogin.html',{'msg':'incorrect username and password'})
                
            else:
                return render(request,'userlogin.html',{'msg':'incorrect username and password'})
            


def vendordashboard(request):
    return render(request,'vendordashboard.html')

def vendorprofile(request):

    vendorsess=request.session['sessionvaluevendor']
    vendorr=vendor.objects.filter(email=vendorsess)
    
    if vendorr:
        vendorobj=vendor.objects.get(email=vendorsess)

    return render(request,'profile.html',{'session':vendorsess,'vendorobj':vendorobj})
def vendoreditprofile(request):
    if request.method == 'GET':
        vendorsess=request.session['sessionvaluevendor']
        vendorr=vendor.objects.get(email=vendorsess)
        return render(request,'vendoreditprofile.html',{'context':vendorr})
    if request.method == 'POST':
        name = request.POST.get('fullname')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phoneno = request.POST.get('phoneno')
        state = request.POST.get('state')
        district = request.POST.get('district')
            
        vendorsess=request.session['sessionvaluevendor']
        vendorr=vendor.objects.filter(email=vendorsess).update(name=name,address=address,phoneno=phoneno,state=state,district=district)
        return redirect('../vendorprofile')

def userprofile(request):

    usersess=request.session['sessionvalue']
    userr=user.objects.filter(email=usersess)
    
    if userr:
        userobj=user.objects.get(email=usersess)

    return render(request,'userprofile.html',{'session':usersess,'vendorobj':userobj})



def usereditprofile(request):
    if request.method == 'GET':
        usersess=request.session['sessionvalue']
        userr=user.objects.get(email=usersess)
        return render(request,'usereditprofile.html',{'context':userr})
    if request.method == 'POST':
        name = request.POST.get('fullname')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phoneno = request.POST.get('phoneno')
        state = request.POST.get('state')
        district = request.POST.get('district')
            
        usersess=request.session['sessionvalue']
        uuserr=user.objects.filter(email=usersess).update(name=name,address=address,phoneno=phoneno,state=state,district=district)
        return redirect('../userprofile')


def addproduct(request):
    categories = category.objects.all()
    subcategories = subcategory.objects.all()
    vendor_email = request.session.get('sessionvaluevendor')
    vendorr = vendor.objects.get(email=vendor_email)
    
    # Check if vendor has an active subscription and determine the subscription level
    try:
        vendor_subscription = VendorSubscriptions.objects.get(vendorid=vendorr)
        subscription_level = vendor_subscription.subscription.name
    except VendorSubscriptions.DoesNotExist:
        subscription_level = None

    # Define upload limits based on subscription levels
    if subscription_level == 'Beginner' and vendorr.product_set.count() >= 10:
        messages.error(request, 'You have reached the limit of 10 products with the Beginner package.')
        return redirect('subscription_plans')
    elif subscription_level == 'Deluxe' and vendorr.product_set.count() >= 50:
        messages.error(request, 'You have reached the limit of 50 products with the Deluxe package.')
        return redirect('subscription_plans')
    elif subscription_level == 'Ultimate' and vendorr.product_set.count() >= 100:
        messages.error(request, 'You have reached the limit of 100 products with the Ultimate package.')
        return redirect('subscription_plans')
    elif subscription_level is None:
        messages.error(request, 'You do not have an active subscription. Please subscribe to upload products.')
        return redirect('subscription_plans')
    
    if request.method == 'POST':
        name = request.POST.get('productname')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        print(image)
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        stock = request.POST.get('stock')

        categoryy = category.objects.get(id=category_id)
        subcategoryy = subcategory.objects.get(id=subcategory_id)

        new_product = product(
            name=name,
            description=description,
            price=price,
            image=image,
            categoryid=categoryy,
            subcategoryid=subcategoryy,
            stock=stock,
            vendorid=vendorr
        )
        new_product.save()

        messages.success(request, 'Product added successfully!')
        return redirect('viewproduct')

    context = {
        'categories': categories,
        'subcategories': subcategories,
    }

    return render(request, 'addproduct.html', context)


def viewproduct(request):
    vendorsess=request.session['sessionvaluevendor']
    
    vendorr=vendor.objects.filter(email=vendorsess)
    if vendorr:

        vendorobj=vendor.objects.get(email=vendorsess)
        pobj=product.objects.filter(vendorid=vendorobj.id)
       

        return render(request,'viewproduct.html',{'pobj':pobj,'session':vendorr})
    
    


# def deleteproduct(request):
#     pid=request.POST.get('productid')
#     vendorsess=request.session['sessionvalue']
#     if vendorsess:
#         vendorr=vendor.objects.get(email=vendorsess)
#         productobj=product.objects.filter(id=pid)
#         productobj.delete()

#     return redirect('../viewproduct')


# class deleteproduct(DeleteView):
#     model = product
#     template_name='deletetask.html'
#     success_url=reverse_lazy('viewproduct')

def delete_product(request,pk):
    donorobj=product.objects.get(id=pk)
    donorobj.delete()
    return redirect('../viewproduct')

class detailproduct(DetailView):
    model =product
    template_name = 'detailviewproduct.html'
    context_object_name='i'




def editproduct(request, pk):
    product_obj = get_object_or_404(product, id=pk)
    categories = category.objects.all()
    subcategories = subcategory.objects.all()

    if request.method == 'POST':
        product_obj.name = request.POST.get('productname')
        product_obj.description = request.POST.get('description')
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        product_obj.categoryid = category.objects.get(id=category_id)
        product_obj.subcategoryid = subcategory.objects.get(id=subcategory_id)
        product_obj.price = request.POST.get('price')
        product_obj.stock = request.POST.get('stock')

        
        if 'image' in request.FILES:
            product_obj.image = request.FILES['image']

        
        product_obj.save()

        return redirect('../viewproduct', product_id=product_obj.id)
    
    context = {
        'product': product,
        'categories': categories,
        'subcategories': subcategories,
        'pobj': product_obj
    }


    return render(request, 'editproduct.html', context)

def vendorlogout(request):
    del(request.session['sessionvaluevendor'])
    return redirect('../vendorlogin')

def userlogout(request):
    del(request.session['sessionvalue'])
    return redirect('../userlogin')


class userviewproduct(ListView):
    model=product
    template_name='userviewproduct.html'
    context_object_name='pobj'
    
    def get_context_data(self, **kwargs) :
        data=self.request.session['sessionvalue']
        context = super().get_context_data(**kwargs)
        context['session']=data
        return context 


def usersearchproduct(request):
    if request.method =="POST":
        searchdata=request.POST.get('searchquery')
        pobj=product.objects.filter(Q(name__icontains = searchdata)|Q(description__icontains = searchdata)|Q(subcategoryid__name__icontains=searchdata)|Q(categoryid__name__icontains=searchdata))
        return render(request,'userviewproduct.html',{'pobj':pobj})
    

def addtocart(request):
    productid=request.POST.get('productid')
    usersession=request.session['sessionvalue']#email of customer
    userobj=user.objects.get(email=usersession)#fetch all record from database table using email
    pobj=product.objects.get(id=productid)
    

    flag=cart.objects.filter(cid=userobj.id,pid=pobj.id)
    if flag:
        cartobj=cart.objects.get(cid=userobj.id,pid=pobj.id)
        cartobj.quantity=cartobj.quantity+1
        cartobj.totalamount=pobj.price*cartobj.quantity
        cartobj.save()
        
    else:
        cartobj=cart(cid=userobj,pid=pobj,quantity=1,totalamount=pobj.price*1)
        cartobj.save()
    return redirect('../userviewproduct') 


def viewcart(request):
    custsession=request.session['sessionvalue']
    custobj=user.objects.get(email=custsession)
    cartobj=cart.objects.filter(cid=custobj.id)

    return render(request,'viewcart.html',{'cartobj':cartobj,'session':custsession})

def changequantity(request):
    cemail = request.session['sessionvalue']
    pid = request.POST.get('pid')

    custobj = user.objects.get(email = cemail)
    pobj = product.objects.get(id = pid)
    cartobj = cart.objects.get(cid = custobj.id,pid=pobj.id)

    if request.POST.get('changequantitybutton')=='+':
        cartobj.quantity = cartobj.quantity + 1
        cartobj.totalamount = cartobj.quantity * pobj.price
        cartobj.save()

    elif request.POST.get('changequantitybutton')=='-':
        if cartobj.quantity == 1:
            cartobj.delete()
        else :
            cartobj.quantity = cartobj.quantity - 1
            cartobj.totalamount = cartobj.quantity * pobj.price
            print(cartobj.totalamount)
            cartobj.save()

    return redirect('../viewcart')


# def detailviewproduct(request):
#     return render(request,'detailviewproduct.html')

def jeansdisplay(request):
    pobj=product.objects.filter(subcategoryid__name='jeans')
    
    return render(request,'displaycategory.html' ,{'pobj':pobj})

def tshirtdisplay(request):
    pobj=product.objects.filter(subcategoryid__name='T-shirt')
    return render(request,'displaycategory.html' ,{'pobj':pobj})


def shirtdisplay(request):
    spobj=product.objects.filter(subcategoryid__name='Shirt')
    return render(request,'displaycategory.html' ,{'pobj':spobj})



def hoodiedisplay(request):
    pobj=product.objects.filter(subcategoryid__name='hoodie')
    return render(request,'displaycategory.html' ,{'pobj':pobj})

def skirtdisplay(request):
    pobj=product.objects.filter(subcategoryid__name='Skirt')
    return render(request,'displaycategory.html' ,{'pobj':pobj})

def displaysweatshirt(request):
    pobj=product.objects.filter(subcategoryid__name='Sweatshirt')
    return render(request,'displaycategory.html' ,{'pobj':pobj})

def displayjacket(request):
    pobj=product.objects.filter(subcategoryid__name='Jacket')
    return render(request,'displaycategory.html' ,{'pobj':pobj})

def displaytrouser(request):
    pobj=product.objects.filter(subcategoryid__name='Trouser')
    return render(request,'displaycategory.html' ,{'pobj':pobj})

def displaytop(request):
    pobj=product.objects.filter(subcategoryid__name='Top')
    return render(request,'displaycategory.html' ,{'pobj':pobj})

def displaydress(request):
    pobj=product.objects.filter(subcategoryid__name='Dress')
    return render(request,'displaycategory.html' ,{'pobj':pobj})

def displaysweater(request):
    pobj=product.objects.filter(subcategoryid__name='Sweater')
    return render(request,'displaycategory.html' ,{'pobj':pobj})

def displayshorts(request):
    pobj=product.objects.filter(subcategoryid__name='Shorts')
    return render(request,'displaycategory.html' ,{'pobj':pobj})



def summary(request):
    custsession=request.session['sessionvalue']
    userobj=user.objects.get(email=custsession)
    cartobj=cart.objects.filter(cid=userobj.id)
    

    totalbill=0
    for i in cartobj:
        totalbill=totalbill + i.totalamount



    return render(request,'summary.html',{'session':custsession,'cartobj':cartobj,'totalbill':totalbill})

def placeorder(request):
    
        firstname=request.POST.get('fn')
        lastname=request.POST.get('ln')
        phoneno=request.POST.get('phoneno')
        address=request.POST.get('address')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        datev= date.today()
        print(datev)
        print(firstname)
        print(lastname)
        print(address)
        custsession=request.session['sessionvalue']
        custobj=user.objects.get(email=custsession)
        cartobj=cart.objects.filter(cid=custobj.id)
        orderobj=order(firstname=firstname, lastname=lastname, phoneno=phoneno, address=address, city=city, state=state, pincode=pincode, orderdate=datev, orderstatus='pending')
        orderobj.save()
        ono=str(orderobj.id) + str(datev).replace('-','')
        orderobj.ordernumber=ono
        orderobj.save()
        
       
        totalbill=0
        for i in cartobj:
            totalbill=totalbill + i.totalamount

        # from django.core.mail import EmailMessage
        # sm=EmailMessage('Order placed','order placed from pet store application.total bill for your order is'+str(totalbill),to=['shubhamtpatil03@gmail.com'])
        # sm.send()

        # return render(request,'payment.html',{'orderobj':orderobj,'session':custsession,'cartobj':cartobj,'totalbill':totalbill})


         
    # authorize razorpay client with API Keys.
        razorpay_client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
 
 

        currency = 'INR'
        amount = 20000  # Rs. 200
 
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
    
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = '../userviewproduct'
    
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZORPAY_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        return render(request,'payment.html',{'orderobj':orderobj,'session':custsession,'cartobj':cartobj,'totalbill':totalbill,'context':context})



def paymentsuccess(request):
    orderid=request.GET.get('order_id')
    tid = request.GET.get('payment_id')
    
    print(orderid)
    print(tid)

    request.session['sessionvalue']=request.GET.get('session')
    usersession=request.session['sessionvalue']
    print(usersession)      
    custobj=user.objects.get(email=usersession)
    cartobj=cart.objects.filter(cid=custobj.id)
    orderobj = order.objects.get(ordernumber = orderid)
    paymentobj=payment(customerid=custobj,oid=orderobj,paymentstatus='complete',transactionid=tid,paymentmode='paypal')
    paymentobj.save()
    oobj=order.objects.filter(ordernumber=orderid).update(orderstatus='order placed')
    
    
    
    for i in cartobj:
        cartqnt=i.quantity
        print(i.pid.id)
        prdqnt=product.objects.get(id=i.pid.id)
        prdqnt.stock=prdqnt.stock-cartqnt
        prdqnt.save()     
            
    
        orderdetailobj=orderdetail(ordernumber=orderobj.ordernumber,customerid=custobj,productid=i.pid,quantity=i.quantity,totalprice=i.totalamount,paymentid=paymentobj)
        orderdetailobj.save()
        

        i.delete()
        # ordobj=orderdetail.objects.filter(customerid=custobj.id)
    return render(request,'paymentsuccess.html',{'session':usersession,'payobj':paymentobj})


def homepage(request):
    usersess=request.session['sessionvalue']
    userobj=user.objects.get(email=usersess)
    return render(request,'homepage.html',{'session':userobj.email})



def subscription_plans(request):
    vendor_email = request.session['sessionvaluevendor']
    vendorr = vendor.objects.get(email=vendor_email)

    subscriptions = Subscription.objects.all()
    vendor_subscriptions = VendorSubscriptions.objects.filter(vendorid=vendorr.id)

    return render(request, 'subscriptionplan.html', {
        'subscriptions': subscriptions,
        'vendor_subscriptions': vendor_subscriptions
    })


def subscribe(request, subscription_id):
    try:
        subscription = Subscription.objects.get(pk=subscription_id)
        vendorr = request.session['sessionvaluevendor']
        vendorobj=vendor.objects.get(email=vendorr)
    except Subscription.DoesNotExist:
        messages.error(request, 'Subscription plan not found.')
        return redirect('subscription_plans')

    current_datetime = datetime.now()

    # Check if the vendor already has an active subscription
    active_subscriptions = VendorSubscriptions.objects.filter(vendorid=vendorobj, end_date__gt=current_datetime)
    if active_subscriptions.exists():
        
        return redirect('subscription_plans')

    # Calculate end date based on subscription duration
    end_date = current_datetime + relativedelta(months=subscription.duration_months)

    # Create VendorSubscription object
    vendor_subscription = VendorSubscriptions(vendorid=vendorobj, subscription=subscription, end_date=end_date)
    vendor_subscription.save()

    
    return redirect('subscription_plans')


def vendor_subscriptions(request):
    vendor_email = request.session['sessionvaluevendor']
    vendorr = vendor.objects.get(email=vendor_email)
    vendor_subscriptions = VendorSubscriptions.objects.filter(vendorid=vendorr.id)

    context = {
        'vendor_subscriptions': vendor_subscriptions,
    }
    return render(request, 'vendor_subscriptions.html', context)


def purchase_subscription(request, subscription_id):
    if request.method == 'POST':
        subscription = get_object_or_404(Subscription, pk=subscription_id)
        
        vendor_email = request.session.get('sessionvaluevendor')
        vendorr = vendor.objects.get(email=vendor_email)
        
        try:
            vendorr = vendor.objects.get(email=vendor_email)
        except vendor.DoesNotExist:
            messages.error(request, 'Vendor not found.')
            return redirect('subscription_plans')

        # Check if the vendor already has an active subscription
        current_datetime = timezone.now()
        active_subscriptions = VendorSubscriptions.objects.filter(vendorid=vendorr, end_date__gt=current_datetime)
        if active_subscriptions.exists():
            messages.error(request, 'You already have an active subscription.')
            return redirect('subscription_plans')

       # authorize razorpay client with API Keys.
        razorpay_client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
 
 

        currency = 'INR'
        amount = 20000  # Rs. 200
 
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
    
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = '../userviewproduct'
    
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZORPAY_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        return render(request, 'vendorpayment.html', {'session':vendor_email,'subscription':subscription,'context':context,'vobj':vendorr})
    else:
        return redirect('subscription_plans')


def payment_success(request):
    order_id = request.GET.get('razorpay_order_id')
    payment_id = request.GET.get('razorpay_payment_id')
    subscription_id = request.GET.get('subid')
    print(subscription_id)
    request.session['sessionvaluevendor']=request.GET.get('session')
    vendor_email=request.session['sessionvaluevendor']
    

    try:
        subscriptions = Subscription.objects.get(pk=subscription_id)
        vendorr = vendor.objects.get(email=vendor_email)
    except (Subscription.DoesNotExist, vendor.DoesNotExist):
        messages.error(request, 'Subscription plan or vendor not found.')
        return HttpResponse('try catch fail')
    

    current_datetime = timezone.now()
    end_date = current_datetime + relativedelta(months=subscriptions.duration_months)
    vendor_subscription = VendorSubscriptions(vendorid=vendorr, subscription=subscriptions, start_date=current_datetime, end_date=end_date)
    vendor_subscription.save()
    vendorobj=vendor.objects.get(email=vendor_email)
    vendorr=VendorSubscriptions.objects.get(vendorid=vendorobj.id)
    vendorpmt=vendorpayment(user_subscription=vendorr,payment_id=payment_id,payment_date=current_datetime,amount=vendorr.subscription.price ,vendorid=vendorobj)
    vendorpmt.save()

    messages.success(request, 'Subscription plan purchased successfully.')
    pymtobj=vendorpayment.objects.get(vendorid=vendorobj.id)
    return render(request,'payment_success.html',{'payobj':pymtobj})
