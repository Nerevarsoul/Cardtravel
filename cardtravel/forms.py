from django import forms
from django.contrib.auth.models import User

from cardtravel.models import UserProfile, Card

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('picture', 'adress')

class CardForm(forms.ModelForm):
	class Meta:
		model = Card
