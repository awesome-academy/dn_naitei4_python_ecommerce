from django.contrib.auth.models import User
import factory
from faker import Factory
from ecommerce.models import Order

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
