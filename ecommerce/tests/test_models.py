from django.test import TestCase
from ecommerce.tests.factories import CategoryFactory, ProductFactory

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = CategoryFactory()
        self.product = ProductFactory(category=self.category)

    def test_product_name_label(self):
        product = self.product
        field_label = product._meta.get_field('product_name').verbose_name
        self.assertEqual(field_label, 'product name')

    def test_category_label(self):
        product = self.product
        field_label = product._meta.get_field('category').verbose_name
        self.assertEquals(field_label, 'category')

    def test_description_label(self):
        product = self.product
        field_label = product._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_price_label(self):
        product = self.product
        field_label = product._meta.get_field('price').verbose_name
        self.assertEquals(field_label, 'price')

    def test_quantity_label(self):
        product = self.product
        field_label = product._meta.get_field('quantity').verbose_name
        self.assertEquals(field_label, 'quantity')

    def test_product_name_max_length(self):
        product = self.product
        max_length = product._meta.get_field('product_name').max_length
        self.assertEquals(max_length, 200)

    def test_description_max_length(self):
        product = self.product
        max_length = product._meta.get_field('description').max_length
        self.assertEquals(max_length, 1000)

    def test_object_name_is_product_name(self):
        product = self.product
        expected_object_name = f'{product.product_name}'
        self.assertEquals(expected_object_name, str(product))

    def test_get_absolute_url(self):
        product = self.product
        self.assertEquals(product.get_absolute_url(), f'/ecommerce/product/{self.product.id}/')
   
    def test_product_required_fields(self):
        product = self.product
        if product.price=='' or product.quantity=='':
            self.assertTrue(product)

    def test_product_not_required_fields(self):
        product = self.product
        if product.product_name=='' and product.category=='' and product.description=='':
            self.assertFalse(product)
    
