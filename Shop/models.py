from django.db import models

from django.utils import timezone
from Users.models import User

# Create your models here.


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10) # in dollar
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    images =  models.CharField(max_length=500, default="")# going to be holding a json list of image names that will help us locate them
    quantity = models.IntegerField(default=0)
    genre = models.CharField(max_length=20)
    brand = models.CharField(max_length=20)
    date_created = models.DateTimeField(default=timezone.now)
    is_featured = models.BooleanField(default=False)




class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.CharField(max_length=500, default="")# in a json string holds a turple of product id and its quantity
    cost = models.IntegerField(default=0)
    is_paid_for = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)