from ecommerce.models import Cart, Product
from django.contrib.auth import models
from django.db.models import fields
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','product_name','image','category','description','publish_date','price','quantity')
