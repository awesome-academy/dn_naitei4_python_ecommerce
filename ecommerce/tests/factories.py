from django.contrib.auth.models import User
import factory
from faker import Factory
from ecommerce import models
from ecommerce.models import Cart, Order, Category, Product, Profile

faker = Factory.create()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user_{n}')
    password =  'mysecret'

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user=factory.SubFactory(UserFactory)
    total_price=faker.random_number()
    shipping_address=faker.address(),
    phone_number=faker.random_number(),
    date=faker.date_object()

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = faker.name()

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    product_name=faker.name()
    category=factory.SubFactory(CategoryFactory)
    description=faker.text()
    price=faker.random_number()
    quantity=faker.random_number()

class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile
        django_get_or_create = ('user',)
    
    user=factory.SubFactory(UserFactory)
    birthday=faker.date_object()
    address=faker.address()

class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    quantity = 1
    product=factory.SubFactory(ProductFactory)
