from ecommerce.models import Cart, Order, Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','product_name','image','category','description','publish_date','price','quantity')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id','user','total_price','shipping_address','phone_number','status')

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('quantity','user','product')
