#!/usr/bin/env python
import os
import sys
import random
import django


def create_users():
	username_list = ['Lantash', 'Shiori', 'Kaito', 'Mio', 'Mia', 
	                 'Cane', 'Sutter', 'Blazi', 'Kitty', 'Nirtok']

	email_list = ['Lantash@gmail.com', 'Shiori@mail.ru', 'Kaito@yandex.ru', 
	              'Mio@gmail.com', 'Mia@gmail.com', 'Cane@mail.ru', 
	              'Sutter@mail.ru', 'Blazi@gmail.com', 'Kitty@mail.ru', 
	              'Nirtok@yandex.ru']

	password_list = ['1q', '2w', '3e', '4r', '5t', '6y', '7u', '8i', '9o', '0p']

	first_name_list = ['Bob', 'Cristy', 'Maya', 'Alex', 'Rodger', 
	                   'Kei', 'Alice', 'Charlie', 'Donna', 'Luis']

	last_name_list = ['Specter', 'Litt', 'Hardman', 'Pirson', 'Depp', 
	                  'Beckham', 'Ross', 'Zein', 'Truman', 'Stalin']

	address_list = ['New York', 'London', 'Paris', 'Rome', 'Berlin', 
	                'Toronto', 'Sydney', 'Deli', 'Pekin', 'Seoul']

	for i in xrange(10):
		user = User.objects.create_user(username_list[i], email_list[i], password_list[i])
		user.last_name = last_name_list[i]
		user.first_name = first_name_list[i]
		user.save()
		profile = UserProfile(user=user)
		profile.address = address_list[i]
		picture = open(os.path.join(MEDIA_ROOT, 'avatar', str(i+2) + '.jpg'))
		profile.picture = File(picture)
		profile.save()


def create_cards():
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

	for card in name_list:
		new_country = random.choice(country)
		new_series = random.choice(series)
		year = random.choice(issued_on)
		catalog_codes = str(name_list.index(card))
		face_picture = open(os.path.join(MEDIA_ROOT, 'cards', card + '.jpg'))
		reverse_picture = open(os.path.join(MEDIA_ROOT, 'cards', card + '-back.jpg'))
		new_card = Card(name=card, country=new_country, series=new_series, 
			            issued_on=year, catalog_codes=catalog_codes, 
			            face_picture=File(face_picture),
			            reverse_picture=File(reverse_picture))
		new_card.save()


	
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    django.setup()

    from django.contrib.auth.models import User
    from django.core.files import File

    from cardtravel.models import UserProfile, Card

    from mysite.settings import MEDIA_ROOT

    create_users()
    create_cards()