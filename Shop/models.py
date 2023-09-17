from django.db import models

from Users.models import User

# Create your models here.


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField(blank=False) # in cent
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    images =  models.CharField(max_length=500)# going to be holding a json list of image names that will help us locate them
    quantity_available = models.IntegerField(blank=False)
    genre = models.CharField(max_length=20)
    brand = models.CharField(max_length=20)




class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.CharField(max_length=500)# in a json string holds a turple of product id and its quantity
    cost = models.IntegerField(default=0) 