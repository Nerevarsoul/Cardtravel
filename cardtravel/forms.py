from django import forms
from django.contrib.auth.models import User

from .models import UserProfile, Card, Trade

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

        def clean_username(self):
            data = self.cleaned_data
            try:
                User.objects.get(username = data['username'])
            except User.DoesNotExist:
                return data['username']
            raise forms.ValidationError('This username is already taken.')

        def clean(self):
            data = self.cleaned_data
            if "password" in data and "password2" in data and \
                data["password"] != data["password2"]:
                    raise forms.ValidationError("Passwords must be same")
                           

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture', 'address')

class CardForm(forms.ModelForm):
    class Meta:
        model = Card

class EditProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    class Meta:
        model = UserProfile
        fields = ('picture', 'address')
