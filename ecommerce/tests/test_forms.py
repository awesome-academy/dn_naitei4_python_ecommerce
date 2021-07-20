from ecommerce.models import Profile
from django.test import TestCase

import datetime
from ..forms import CommentForm, ProfileForm, ReviewForm, UserForm


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

class ReviewFormTest(TestCase):
    def test_rate_bigger_than_five(self):
        """Test form is invalid if rate bigger more than five stars."""
        rate = "6"
        form = ReviewForm(data={'rate': rate})
        self.assertFalse(form.is_valid())

    def test_rate_smaller_than_one(self):
        """Test form is invalid if rate smaller more than five stars."""
        rate = "0"
        form = ReviewForm(data={'rate': rate})
        self.assertFalse(form.is_valid())

    def test_rate_is_not_digit(self):
        """Test form is invalid if rate value is not digit."""
        rate = "4.13"
        form = ReviewForm(data={'rate': rate})
        self.assertFalse(form.is_valid())

    def test_rate_field_label(self):
        """Test rate label is 'rate'."""
        form = ReviewForm()
        self.assertTrue(
            form.fields['rate'].label is None or
            form.fields['rate'].label == 'rate')

    def test_title_field_label(self):
        """Test title label is 'title'."""
        form = ReviewForm()
        self.assertTrue(
            form.fields['title'].label is None or
            form.fields['title'].label == 'title')

    def test_content_field_label(self):
        """Test content label is 'content'."""
        form = ReviewForm()
        self.assertTrue(
            form.fields['content'].label is None or
            form.fields['content'].label == 'content')
    
    def test_review_form_required_fields(self):
        form = ReviewForm(data={'title': '', 'content': ''})
        self.assertFalse(form.is_valid())

class ReviewFormTest(TestCase):
    def test_comment_field_label(self):
        """Test comment label is 'comment'."""
        form = CommentForm()
        self.assertTrue(
            form.fields['comment'].label is None or
            form.fields['comment'].label == 'comment')
    
    def test_comment_form_required_fields(self):
        form = ReviewForm(data={'comment': ''})
        self.assertFalse(form.is_valid())
