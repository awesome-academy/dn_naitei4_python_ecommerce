from django.test import TestCase
from django.contrib.auth.models import Permission, User
from django.urls.base import reverse
from .test_setup import TestSetUp
from ecommerce.tests.factories import CartFactory, CommentFactory, OrderFactory, ProductFactory, ReviewFactory

class CheckOrderAllListViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()

        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        test_user2.save()

        permission = Permission.objects.get(name='Set order as returned')
        test_user1.user_permissions.add(permission)
        test_user1.save()

        # Create an Order object for test_user2
        self.test_order1 = OrderFactory(user=test_user1)

        # Create an Order object for test_user2
        self.test_order2 = OrderFactory(user=test_user2)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('all-order'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_order_all_url_exists(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/ecommerce/order/all/')
        self.assertEqual(response.status_code, 200)

    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('all-order'))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_with_permission_another_users_order(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('all-order'))

        # Check that it lets us login. We're a manager, so we can view any users order
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('all-order'))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'ecommerce/order_list_all.html')

class OrderViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='1X<ISRUkw+tuK')
        test_user.save()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/ecommerce/order/')
        self.assertEqual(response.status_code, 302)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('order_get'))
        self.assertEqual(response.status_code, 302)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('order_get'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_logged_in(self):
        login = self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        response = self.client.get(reverse('order_get'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        response = self.client.get(reverse('order_get'))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'ecommerce/order.html')

class OrderDetailViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='1X<ISRUkw+tuK')
        test_user.save()

        self.test_order = OrderFactory(user=test_user)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('order_detail', kwargs={'pk': self.test_order.pk}))
        self.assertEqual(response.status_code, 302)

    def test_logged_in(self):
        login = self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        response = self.client.get(reverse('order_detail', kwargs={'pk': self.test_order.pk}))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        response = self.client.get(reverse('order_detail', kwargs={'pk': self.test_order.pk}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'ecommerce/order_detail.html')

class ProductSearchViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/ecommerce/search')
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('product_search'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse('product_search'))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'ecommerce/product_list.html')

class ProductGetViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/ecommerce/')
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'ecommerce/product_list.html')

class CartCheckoutViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='1X<ISRUkw+tuK')
        test_user.save()

        self.test_product = ProductFactory(quantity='0')
        self.test_cart = CartFactory(product=self.test_product, quantity='1')
        self.test_order = OrderFactory(user=test_user)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('cart_checkout'))
        self.assertEqual(response.status_code, 302)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('cart_checkout'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_logged_in(self):
        login = self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        response = self.client.get(reverse('cart_checkout'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        response = self.client.get(reverse('cart_checkout'))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'ecommerce/checkout.html')

    def test_product_out_of_stock_validate(self):
        self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        self.client.get(reverse('cart_add', kwargs={'pk': self.test_product.pk}))
        response = self.client.get('/ecommerce/cart/checkout')
        self.assertRedirects(response, '/ecommerce/cart' , status_code=404, msg_prefix=f"{self.test_product.product_name} is out of stock limit, please decrease your product items in your cart")

    def test_order_infomation_null(self):
        self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        response = self.client.get('/ecommerce/cart/checkout')
        self.assertRedirects(response,'/ecommerce/cart', status_code=404, msg_prefix="Shipping address or phone number is invalid!")

    def test_post_order_information_null(self):
        self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        response = self.client.post('/ecommerce/cart/checkout')
        self.assertRedirects(response, reverse('cart_checkout') , status_code=301, msg_prefix="Shipping address or phone number is invalid!")
    
    def test_post_order_information_success(self):
        self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        response = self.client.post('/ecommerce/cart/checkout', data={"shipping_address": self.test_order.shipping_address, "phone_number":self.test_order.phone_number})
        new_order = self.client.get(reverse('order_detail', kwargs={'pk': self.test_order.pk}))
        self.assertEqual(str(new_order.context['total_price']), self.test_order.total_price)
        self.assertRedirects(response, reverse('products') , status_code=200, msg_prefix="Order is waiting for being approved by admin! Please wait the approve message!")

class CartViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='1X<ISRUkw+tuK')
        test_user.save()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/ecommerce/cart/')
        self.assertEqual(response.status_code, 302)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('cart_get'))
        self.assertEqual(response.status_code, 302)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('cart_get'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_logged_in(self):
        login = self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        response = self.client.get(reverse('cart_get'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        response = self.client.get(reverse('cart_get'))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'ecommerce/cart.html')

class CartAddViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='1X<ISRUkw+tuK')
        test_user.save()

        self.test_product = ProductFactory()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('cart_add', kwargs={'pk': self.test_product.pk}))
        self.assertEqual(response.status_code, 302)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('cart_add', kwargs={'pk': self.test_product.pk}))
        self.assertEqual(response.status_code, 302)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('cart_add', kwargs={'pk': self.test_product.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

class ProfileViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='1X<ISRUkw+tuK')
        test_user.save()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/ecommerce/profile/')
        self.assertEqual(response.status_code, 404)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('get-profile'))
        self.assertEqual(response.status_code, 302)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('get-profile'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_logged_in(self):
        login = self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        response = self.client.get(reverse('get-profile'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        response = self.client.get(reverse('get-profile'))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'ecommerce/profile.html')

class ProfileUpdateViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()

        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        test_user2.save()

        permission = Permission.objects.get(name='Set order as returned')
        test_user1.user_permissions.add(permission)
        test_user1.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('update-profile'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_logged_in(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('update-profile'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('update-profile'))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'ecommerce/profile.html')

    def test_redirects_to_profile_update_on_success(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        first_name, last_name, email = 'Nguyen', 'Nabi', 'nabi@email.com'
        response = self.client.post(reverse('update-profile'),
                                    {'first_name': first_name,
                                     'last_name': last_name,
                                     'email': email})
        self.assertEqual(response.status_code, 200)

class ReviewAddViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='1X<ISRUkw+tuK')
        test_user.save()

        self.test_product = ProductFactory()
        self.test_review = ReviewFactory()

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        response = self.client.get(reverse('review_add', kwargs={'pk': self.test_product.pk}))
        self.assertEqual(response.status_code, 302)
           
    def test_view_url_accessible_by_name(self):
        self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        response = self.client.get(reverse('review_add', kwargs={'pk': self.test_product.pk}))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect_if_not_have_pk(self):
        self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        response = self.client.get(reverse('review_add'))
        self.assertEqual(response.status_code, 404)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('review_add', kwargs={'pk': self.test_product.pk}))
        self.assertEqual(response.status_code, 404)
    
    def test_uses_correct_template(self):
        self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        response = self.client.get(reverse('review_add', kwargs={'pk': self.test_product.pk}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'ecommerce/product_detail.html')

    def test_post_review_success(self):
        self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        response = self.client.post(reverse('review_add', kwargs={'pk': self.test_product.pk}), data={"title": self.test_review.title, "content":self.test_review.content, "rate":self.test_review.rate})
        new_review = self.client.get(reverse('product-detail', kwargs={'pk': self.test_product.pk}))
        self.assertEqual(str(new_review.context['title']), self.test_review.title)
        self.assertEqual(str(new_review.context['content']), self.test_review.content)

class CommentAddViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='1X<ISRUkw+tuK')
        test_user.save()

        self.test_review = ReviewFactory()
        self.test_comment = CommentFactory()

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        response = self.client.get(reverse('comment_add', kwargs={'pk': self.test_review.pk}))
        self.assertEqual(response.status_code, 302)
           
    def test_view_url_accessible_by_name(self):
        self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        response = self.client.get(reverse('comment_add', kwargs={'pk': self.test_review.pk}))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect_if_not_have_pk(self):
        self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        response = self.client.get(reverse('comment_add'))
        self.assertEqual(response.status_code, 404)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('comment_add', kwargs={'pk': self.test_review.pk}))
        self.assertEqual(response.status_code, 404)
    
    def test_uses_correct_template(self):
        self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        response = self.client.get(reverse('comment_add', kwargs={'pk': self.test_review.pk}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'ecommerce/review_detail.html')

    def test_post_review_success(self):
        self.client.login(username = 'testuser', password = '1X<ISRUkw+tuK')
        response = self.client.post(reverse('comment_add', kwargs={'pk': self.test_review.pk}), data={"comment": self.test_comment.comment})
        new_comment = self.client.get(reverse('review-detail', kwargs={'pk': self.test_review.pk}))
        self.assertEqual(str(new_comment.context['comment']), self.test_comment.comment)

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
