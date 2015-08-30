from django import forms
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button

from .models import UserProfile, Card, Trade

class UserForm(forms.ModelForm):

    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    picture = forms.ImageField(required=False)
    address = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 
                  'picture', 'address')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-4'
        button = Button('send_button', 'Sign up')
        button.input_type = 'submit'
        button.field_classes = 'btn btn-success form-control'
        self.helper.add_input(button)

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
                           

class LoginForm(forms.Form):

    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline'
        button = Button('send_button', 'Sign in')
        button.input_type = 'submit'
        button.field_classes = 'btn btn-success form-control'
        self.helper.add_input(button)


class CardForm(forms.ModelForm):
    class Meta:
        model = Card


class EditProfileForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-4'
        button = Button('send_button', 'Edit')
        button.input_type = 'submit'
        button.field_classes = 'btn btn-success form-control'
        self.helper.add_input(button)

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = UserProfile
        fields = ('picture', 'address')

    def clean_username(self):
        data = self.cleaned_data
        try:
            User.objects.get(username = data['username'])
        except User.DoesNotExist:
            return data['username']
        raise forms.ValidationError('This username is already taken.')
