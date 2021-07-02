from django.test import TestCase
from django.contrib.auth.models import Permission
from django.urls.base import reverse
from ecommerce.tests.factories import OrderFactory, UserFactory

class CheckOrderAllListViewTest(TestCase):
    def setUp(self):
        self.test_user1 = UserFactory(id=1)
        self.test_user2 = UserFactory(id=2)
        
        self.test_user1.save()
        self.test_user2.save()

        permission = Permission.objects.get(name='Set order as returned')
        self.test_user2.user_permissions.add(permission)
        self.test_user2.save()

        # Create an Order object for test_user1
        self.test_order1 = OrderFactory(user=self.test_user1)

        # Create an Order object for test_user2
        self.test_order2 = OrderFactory(user=self.test_user2)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('all-order'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_order_all_url_exists(self):
        login = self.client.login(username = self.test_user2.username, password = self.test_user2.password)
        response = self.client.get('/ecommerce/order/all/')
        self.assertEqual(response.status_code, 302)

    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username = self.test_user1.username, password = self.test_user1.password)
        response = self.client.get(reverse('all-order'))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_with_permission_another_users_order(self):
        login = self.client.login(username = self.test_user2.username, password = self.test_user2.password)
        response = self.client.get(reverse('all-order'))

        # Check that it lets us login. We're a manager, so we can view any users order
        self.assertEqual(response.status_code, 302)
