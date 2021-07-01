from django.contrib.auth.models import User
import factory
from faker import Factory
from ecommerce.models import Order, Category, Product

faker = Factory.create()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda t: faker.name())
    password = factory.PostGenerationMethodCall('set_password', 'mysecret')

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
