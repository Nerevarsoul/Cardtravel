from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import UserProfile, Card, Trade, Comment


# Create your tests here.
class URLTests(TestCase):

    def setUp(self):
        User.objects.get_or_create(username='Lantash', 
                                   email='Lantash@gmail.com',
                                   password='1q')
        user = User.objects.get(id=1)
        UserProfile.objects.get_or_create(user=user)

    def test_index_page(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    #mistake!!!!!!
    def test_edit_profile_page(self):
        url = reverse('edit_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_register_page(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    #mistake!!!!!!
    def test_view_profile_page(self):
        url = reverse('view_profile', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_users_page(self):
        url = reverse('users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_cardlist_page(self):
        url = reverse('view_cardlist', kwargs={"user_id": 1, 
                                               "list_category": 'wishlist'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)