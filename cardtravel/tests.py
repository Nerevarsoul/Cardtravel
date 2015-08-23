import os
import random

from django.contrib.auth.models import User
from django.core.files import File
from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import UserProfile, Card, Trade, Comment
from mysite.settings import MEDIA_ROOT


name_list = ['Christmas', 'Christmas-Tree', 'Coffee-Aroma', 
                 'Cup-of-coffee', 'Frappucino-Card', 'London-old-logo--lt',
                 'Love-Birds', 'Nested-doll', 'Seattle-mini', 'Snowflake',
                 'Snowman', 'Snowman-2012', 'Spring-Blossom', 
                 'Valentine--s-Mini-Set-2015',]

country = ['Unated State of America', 'Russia', "Great Britan", 'Japan',
                'Thailand', "India"]

series = ['Christmas Series', 'Starbucks', 'Special Edition', 
              'Regional Series', 'Small card']

issued_on = [2001, 2003, 2005, 2009, 2010, 2012]


# Create your tests here.
class URLTests(TestCase):

    def setUp(self):
        User.objects.get_or_create(username='Lantash', 
                                   email='Lantash@gmail.com',
                                   password='1q')
        user = User.objects.get(id=1)
        UserProfile.objects.get_or_create(user=user)

        for card in name_list:
            new_country = random.choice(country)
            new_series = random.choice(series)
            year = random.choice(issued_on)
            catalog_codes = str(name_list.index(card))
            face_picture = open(os.path.join(MEDIA_ROOT, 'cards', 
                                             card + '.jpg'))
            reverse_picture = open(os.path.join(MEDIA_ROOT, 'cards', 
                                                card + '-back.jpg'))
            Card.objects.get_or_create(name=card, 
                                       country=new_country, 
                                       series=new_series, 
                                       issued_on=year, 
                                       catalog_codes=catalog_codes, 
                                       face_picture=File(face_picture),
                                       reverse_picture=File(reverse_picture))

        card = Card.objects.get(id=1)
        face_picture = open(os.path.join(MEDIA_ROOT, 'cards', 
                                             card.name + '.jpg'))
        Trade.objects.get_or_create(user=user, card=card, condition="mint",
                                    face_picture=File(face_picture))
    
    def test_index_page(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # testing profile urls
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

    # testing cards urls
    def test_cards_page(self):
        url = reverse('cards')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_card_page(self):
        url = reverse('view_card', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_category_page(self):
        url = reverse('view_category', kwargs={"category": "country", 
                                               "category_url": 'Russia'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # testing trades urls
    def test_trades_page(self):
        url = reverse('trades')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_trade_page(self):
        url = reverse('view_trade', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_tradelist_page(self):
        url = reverse('view_tradelist', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_trade_card_page(self):
        url = reverse('view_trade_card', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)