from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(null=True, blank=True, upload_to='images/', default='avatar.png')
    date = models.DateField(default='2022-01-01')

class Product(models.Model):
    product_img = models.ImageField(null=False, blank=False, upload_to='products/', default='github.png')
    product_name = models.CharField(max_length = 50)
    product_des = models.CharField(max_length=100)
    product_price = models.IntegerField()
