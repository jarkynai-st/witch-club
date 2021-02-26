from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Product(models.Model):
    categories = (
        ('sweatshirt','sweatshirt'),
        ('shoes','shoes'),
        ('t-shirt','t-shirt'),
        ('dress','dress'),
        ('costume','costume'),
        ('jeans','jeans'),
    )
    sizes = (
        ('S','S'),
        ('M','M'),
        ('L','L'),
    )
    genders = (
        ('Male','Male'),
        ('Female','Female'),
    )
    name = models.CharField(max_length=40)
    category = models.CharField(max_length=40,choices=categories)
    price = models.FloatField()
    size = models.CharField(choices=sizes,max_length=50)
    gender = models.CharField(max_length=20, choices=genders)
    image = models.ImageField()
    sale = models.BooleanField()
    sale_amount = models.IntegerField(default=0)
    description = models.TextField()



class Order(models.Model):
    statuses = (
        ('delivered','delivered'),
        ('not_delivered','not_delivered'),
        ('in_process','in_process'),
    )
    payment_methods = (
        ('Wall','Wall'),
        ('Nul','Nul'),
    )
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    payment_type = models.CharField(max_length=20, choices=payment_methods)
    status = models.CharField(max_length=40, choices=statuses, default='in process')
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)


class Contact(models.Model):
    name = models.CharField(max_length=30)
    phone = models.IntegerField()
    email = models.EmailField()
    street = models.CharField(max_length=20)




