from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(label='Login')
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class CreateUserForm(forms.Form):
    username = forms.CharField(label='Login')
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password_repeated = forms.CharField(label="Password repeated", widget=forms.PasswordInput)
    email = forms.CharField(label='email', widget=forms.EmailInput)
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')

    def clean(self):
        if not self.cleaned_data['password'] == self.cleaned_data['password_repeated']:
            raise ValidationError('Passwords are not the same!')

        return self.cleaned_data
