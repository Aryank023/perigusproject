from django.contrib import admin
from .models import product,category,subcategory,Subscription,VendorSubscriptions
# Register your models here.

admin.site.register(product)
admin.site.register(category)
admin.site.register(subcategory)
admin.site.register(Subscription)
admin.site.register(VendorSubscriptions)

