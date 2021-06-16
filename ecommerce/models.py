from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=200, help_text=_('Enter a product category (e.g. Fashion Toy)'))

    def __str__(self):
        return self.name

class Product(models.Model):
    product_name = models.CharField(max_length=200)
    image = models.ImageField(default='/product_pics/default.png', upload_to='product_pics')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    description = models. TextField(max_length=1000, help_text=_('Enter a brief description of the product'))
    publish_date = models.DateField(null=True, blank=True)
    price = models.FloatField(blank=True, null=True)
    quantity = models.IntegerField(null=True, default=1)

    def __str__(self):
        return self.product_name

class User(models.Model):
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    image = models.ImageField(default='/profile_pics/default.jpg', upload_to='profile_pics')
    birthday = models.DateField(null=True,blank=True)
    address = models.CharField(max_length=200)
    ROLE = (
        ('U','user'),
        ('M','manager')
    )
    role = models.CharField(choices=ROLE, max_length=2, blank=True, default=ROLE[0][0], help_text='User role')
    
    def __str__(self):
        return self.username

class Order(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)
    total_price = models.FloatField(blank=True, null= True, default=0)
    date = models.DateField(null=True, blank=True)
    BOOKING_STATUS = (
        ('W','waiting'),
        ('A','approved'),
        ('R','rejected')
    )
    status = models.CharField(choices=BOOKING_STATUS, max_length=2, blank=True, default=BOOKING_STATUS[0][0], help_text='Booking state')

    def __str__(self):
        return self.user.username

class FavoriteProduct(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)
    is_favorited = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Booking(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, null=True)
