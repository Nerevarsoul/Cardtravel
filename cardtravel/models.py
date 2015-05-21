from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User)

	picture = models.ImageField(upload_to='profile_images', blank=True)
	adress = models.TextField(blank=True)

	def __unicode__(self):
		return self.user.username

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
