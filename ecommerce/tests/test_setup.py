from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

class TestSetUp(APITestCase):
    def setUp(self):
        self.product_url = '/products/'
        self.product_data = {
            'product_name': 'Pant',
            'description': 'Nice',
            'price': 100.0,
            'quantity': 100,
            }
        self.checkout_url = '/checkout/'
        self.order_data = {
            'shipping_address': 'abc',
            'phone_number' : '123',
        }
        self.user = self.setup_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        return super().setUp()
    
    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create(username='user1', password='user1', email='user1@mail.com')
