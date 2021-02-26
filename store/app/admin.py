from django.contrib import admin

from .models import Product, Order, Contact

# Register your models here.


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Contact)