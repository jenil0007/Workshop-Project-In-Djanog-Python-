from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(null=True, blank=True, upload_to='images/')
    date = models.DateField(default='01-01-2022')

class Product(models.Model):
    product_img = models.ImageField(null=False, blank=False, upload_to='products/', default='github.png')
    product_name = models.CharField(max_length = 50)
    product_des = models.CharField(max_length=100)
    product_price = models.IntegerField()
