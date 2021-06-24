from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save

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

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    total_price = models.FloatField(blank=True, null= True, default=0)
    shipping_address = models.CharField(max_length=200, null= True, help_text=_('Enter your shipping address (e.g. Danang, VietNam)'))
    phone_number = models.CharField(max_length=20, null= True, help_text=_('Enter your phone number (e.g. 840247xxx )'))
    total_price = models.IntegerField(default=0)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)
    is_favorited = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Booking(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, null=True)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birthday = models.DateField(null=True,blank=True)
    address = models.CharField(max_length=200,null=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Cart(models.Model):
    quantity = models.IntegerField(db_column='quantity')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)

    def get_total_price(self):
        return self.quantity*self.product.price
