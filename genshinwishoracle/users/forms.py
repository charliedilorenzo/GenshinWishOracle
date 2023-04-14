from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from .models import Profile

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    # get current user and display their current values? TODO
    numprimos = forms.IntegerField(min_value=0, required=False,  widget=forms.NumberInput(attrs={'class': 'form-control'}))
    numgenesis = forms.IntegerField(min_value=0, required=False,  widget=forms.NumberInput(attrs={'class': 'form-control'}))
    numfates = forms.IntegerField(min_value=0, required=False,  widget=forms.NumberInput(attrs={'class': 'form-control'}))
    numstarglitter = forms.IntegerField(min_value=0, required=False,  widget=forms.NumberInput(attrs={'class': 'form-control'}))

    character_pity = forms.IntegerField(min_value=0, max_value=89, required=False,  widget=forms.NumberInput(attrs={'class': 'form-control'}))
    character_guaranteed = forms.BooleanField(required=False)

    weapon_pity = forms.IntegerField(min_value=0, max_value=79, required=False,  widget=forms.NumberInput(attrs={'class': 'form-control'}))
    weapon_guaranteed = forms.BooleanField(required=False)
    weapon_fate_points = forms.IntegerField(min_value=0, max_value=2, required=False,  widget=forms.NumberInput(attrs={'class': 'form-control'}))

    welkin_user = forms.BooleanField(required=False)
    battlepass_user = forms.BooleanField(required=False )

    class Meta:
        model = Profile
        fields = ['numprimos', 'numgenesis','numfates','numstarglitter','character_pity','character_guaranteed','weapon_pity', 'weapon_guaranteed','weapon_fate_points', 'welkin_user','battlepass_user']

class LoginForm(AuthenticationForm):
    # get current user and display their current values? TODO
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']
class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
