from ecommerce.models import Profile
from django.test import TestCase

import datetime
from ..forms import ProfileForm, UserForm


class ProfileFormTest(TestCase):
    def test_birthday_too_far_in_future(self):
        """Test form is invalid if birthday more than from today."""
        date = datetime.date.today() + datetime.timedelta(days=1)
        form = ProfileForm(data={'birthday': date})
        self.assertFalse(form.is_valid())

    def test_birthday_field_label(self):
        """Test birthday label is 'birthday'."""
        form = ProfileForm()
        self.assertTrue(
            form.fields['birthday'].label is None or
            form.fields['birthday'].label == 'birthday')

    def test_address_field_label(self):
        """Test address label is 'address'."""
        form = ProfileForm()
        self.assertTrue(
            form.fields['address'].label is None or
            form.fields['address'].label == 'address')
    
    def test_address_required_fields(self):
        form = ProfileForm(data={'birthday': '', 'address': ''})
        self.assertFalse(form.is_valid())

class UserFormTest(TestCase):

    def test_username_field_label(self):
        """Test username label is 'username'."""
        form = UserForm()
        self.assertTrue(
            form.fields['username'].label is None or
            form.fields['username'].label == 'Username')
            
    def test_address_required_fields(self):
        form = ProfileForm(data={'username': '', 'first_name': '','last_name':'','email':''})
        self.assertFalse(form.is_valid())
