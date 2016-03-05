from django.contrib.auth.models import User
from .models import Player, Developer, Game
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from storeapp.validators.price_validator import *


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {
            'username': 'Username has to be less than 30 characters'
        }

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class PlayerRegForm(ModelForm):
    class Meta:
        model = Player
        exclude = ['user', 'games']


class DevRegForm(ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = Developer
        exclude = ['user', 'games']
        fields = ['first_name', 'last_name', 'iban']
        labels = {
            'iban': 'IBAN'
        }


class GameForm(forms.ModelForm):
    name = forms.CharField(label='Name', max_length=30)
    url = forms.URLField(label='URL')
    price = forms.FloatField(label='Price', validators=[validate_price])
    genre = forms.ChoiceField(choices=Game.GENRE_CHOICES, label='Genre', required=True, widget=forms.Select())

    class Meta:
        model = Game
        fields = ['name', 'url', 'price', 'genre']


class SocialSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)
        help_texts = {
            'username': 'Username has to be less than 30 characters'
        }

