from django.db import models
from datetime import datetime ,timedelta
from django.utils import timezone
from dateutil.relativedelta import relativedelta 
from pathlib import os
# Create your models here.
class user(models.Model):
    name= models.CharField(max_length=50)
    age = models.BigIntegerField()
    gender = (('Male','male'),('Female','female'),('Other','other'))
    gender = models.CharField(max_length=20, choices=gender)
    phoneno= models.BigIntegerField()
    address = models.TextField(max_length=200)
    state = models.CharField(max_length=50)
    district= models.CharField(max_length=50)
    pincode = models.BigIntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=500)

    class Meta:
        db_table= 'user'

class vendor(models.Model):
    name= models.CharField(max_length=50)
    age = models.BigIntegerField()
    gender = (('Male','male'),('Female','female'),('Other','other'))
    gender = models.CharField(max_length=20, choices=gender)
    phoneno= models.BigIntegerField()
    address = models.TextField(max_length=200)
    state = models.CharField(max_length=50)
    district= models.CharField(max_length=50)
    pincode = models.BigIntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=500)

    class Meta:
        db_table= 'vendor'


def default_date():
    unformat=datetime.now().date() + timedelta(days=1)
    formatted_date=unformat.strftime("%d/%B/%Y")
    return formatted_date

def filepath(request,filename):
    old_filename=filename
    timeNow=datetime.now().strftime("%Y%m%d%H%M%S")
    filename="%s%s" % (timeNow,old_filename)
    return os.path.join('media',filename)

class category(models.Model):
    name=models.CharField(max_length=100)

    class Meta:
        db_table='category'

class subcategory(models.Model):
    name=models.CharField(max_length=100)
    

    class Meta:
        db_table='subcategory'



class product(models.Model):
    vendorid=models.ForeignKey(vendor,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=filepath,null=False,blank=False)
    categoryid=models.ForeignKey(category,on_delete=models.CASCADE)
    subcategoryid=models.ForeignKey(subcategory,on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    STATUS_CHOICES = (
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default="pending")


    class Meta:
        db_table='product'


class cart(models.Model):
    cid=models.ForeignKey(user,on_delete=models.CASCADE)
    pid=models.ForeignKey(product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    totalamount=models.FloatField()



    class Meta:
        db_table='cart'


class order(models.Model):

    ordernumber = models.CharField(max_length=100)  
    orderdate=models.DateField()
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    phoneno=models.BigIntegerField()
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    pincode=models.BigIntegerField()
    orderstatus=models.CharField(max_length=100)

    class Meta:
        db_table='order'


class payment(models.Model):
    customerid=models.ForeignKey(user,on_delete=models.CASCADE)
    oid=models.ForeignKey(order,on_delete=models.CASCADE)
    paymentstatus=models.CharField(max_length=100,default='pending')
    transactionid=models.CharField(max_length=200)
    paymentmode=models.CharField(max_length=100,default='paypal')


    class Meta:
        db_table='payment'



class orderdetail(models.Model):
    ordernumber=models.CharField(max_length=100)
    customerid=models.ForeignKey(user,on_delete=models.CASCADE)
    productid=models.ForeignKey(product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    totalprice=models.IntegerField()
    paymentid=models.ForeignKey(payment,on_delete=models.CASCADE)
    created_at=models.DateField(auto_now=True)
    updated_at=models.DateField(auto_now=True)

    class Meta:
        db_table='orderdetail'



class Subscription(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_months = models.IntegerField()  # Duration in months
    features = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table='Subscription'


class VendorSubscriptions(models.Model):
    vendorid = models.ForeignKey(vendor, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Calculate end date based on subscription duration
        self.end_date = self.start_date + relativedelta(months=self.subscription.duration_months)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.subscription.name}"
    
    class Meta:
        db_table='vendorsubscriptions'







class vendorcart(models.Model):
    customer = models.ForeignKey(vendor, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    totalamount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.customer.username} - {self.subscription.name}"
    
    class Meta:
        db_table='vendorcart'


class vendororder(models.Model):
    customer = models.ForeignKey(vendor, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phoneno = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    orderdate = models.DateField(auto_now_add=True)
    ordernumber = models.CharField(max_length=20, unique=True)
    orderstatus = models.CharField(max_length=20)

    def __str__(self):
        return f"Order {self.ordernumber}"
    
    class Meta:
        db_table='vendororder'


class vendororderdetail(models.Model):
    ordernumber=models.CharField(max_length=100)
    customerid=models.ForeignKey(user,on_delete=models.CASCADE)
    subscriptionid=models.ForeignKey(Subscription,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    totalprice=models.IntegerField()
    paymentid=models.ForeignKey(payment,on_delete=models.CASCADE)
    created_at=models.DateField(auto_now=True)
    updated_at=models.DateField(auto_now=True)

    class Meta:
        db_table='vendororderdetail'

class vendorpayment(models.Model):
    vendorid=models.ForeignKey(vendor,on_delete=models.CASCADE)
    user_subscription = models.ForeignKey(VendorSubscriptions, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_id = models.CharField(max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.user_subscription.subscription.name} by {self.user_subscription.user.username}"
    
    class Meta:
        db_table='vendorpayment'