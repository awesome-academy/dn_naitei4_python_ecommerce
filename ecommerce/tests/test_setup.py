from rest_framework.test import APITestCase

class TestSetUp(APITestCase):
    def setUp(self):
        self.product_url = '/products/'
        self.product_data = {
            'product_name': 'Pant',
            'description': 'Nice',
            'price': 100.0,
            'quantity': 100,
            }
        
        return super().setUp()
