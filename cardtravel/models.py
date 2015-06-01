from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile")

    picture = models.ImageField(upload_to='profile_images', blank=True)
    adress = models.TextField(blank=True)

    def __unicode__(self):
    	return self.user.username

    def get_wishlist(self):
    	wishlist = self.user.wishlist.wishlist.all()
    	return wishlist

    def get_collection(self):
    	collection = self.user.collection.collectionlist.all()
    	return collection


class Card(models.Model):
	name = models.CharField(max_length=50)
	country = models.CharField(max_length=50)
	series = models.CharField(max_length=50)
	catalog_codes = models.CharField(max_length=50)
	issued_on = models.IntegerField()
	description = models.TextField(blank=True)
	face_picture = models.ImageField(upload_to='card_images', blank=True)
	reverse_picture = models.ImageField(upload_to='card_images', blank=True)

	def __unicode__(self):
		return self.name


class WishList(models.Model):
	user = models.OneToOneField(User)
	wishlist = models.ManyToManyField(Card, blank=True, null=True)

	def __unicode__(self):
		return self.user.username + "'s wishlist"


class Collection(models.Model):
	user = models.OneToOneField(User)
	collectionlist = models.ManyToManyField(Card, blank=True, null=True)

	def __unicode__(self):
		return self.user.username + "'s collection"