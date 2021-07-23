from ecommerce.tests.test_setup import TestSetUp

class TestProductAPI(TestSetUp):
    def test_list_success(self):
        response = self.client.get(self.product_url)
        self.assertEqual(response.status_code, 200)

    def test_create_successful(self):
        response = self.client.post(self.product_url, self.product_data, format='json')
        res_data = response.data
        self.assertEqual(res_data['product_name'], self.product_data['product_name'])
        self.assertEqual(res_data['description'], self.product_data['description'])
        self.assertEqual(res_data['price'], self.product_data['price'])
        self.assertEqual(res_data['quantity'], self.product_data['quantity'])
        self.assertEqual(response.status_code, 201)

    def test_create_invalid_data(self):
        invalid_data = self.product_data
        invalid_data['product_name'] = ''
        response = self.client.post(self.product_url, invalid_data, format='json')
        self.assertEqual(response.status_code, 400)
