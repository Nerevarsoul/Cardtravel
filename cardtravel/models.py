import datetime

from django.db import models
from django.contrib.auth.models import User


def encode_url(raw_url):
    return raw_url.replace(' ', '_')


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

    def get_absolute_url(self):
        return "/cards/%i/" % self.id


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


class Trade(models.Model):

    CONDITION = (
        ('mint', ('mint')), 
        ('mint+', ('mint+')), 
        ('mint--', ('mint--')), 
        ('mint-', ('mint-')),
    )

    user = models.ForeignKey(User)
    card = models.ForeignKey(Card)
    condition = models.CharField(choices=CONDITION, max_length=20)
    description = models.TextField(blank=True)
    face_picture = models.ImageField(upload_to='trade_images')
    reverse_picture = models.ImageField(upload_to='trade_images', blank=True, default=None)
    addiction_picture1 = models.ImageField(upload_to='trade_images', blank=True, default=None)
    addiction_picture2 = models.ImageField(upload_to='trade_images', blank=True, default=None)
    addiction_picture3 = models.ImageField(upload_to='trade_images', blank=True, default=None)
    date = models.DateTimeField(auto_now=True, default = datetime.datetime.now())

    def __unicode__(self):
        return self.card.name + ' ' + self.condition

    def get_absolute_url(self):
        return "/trades/%i/" % self.id

