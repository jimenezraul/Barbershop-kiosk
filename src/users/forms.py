from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    username = forms.CharField(label='',
                    widget=forms.TextInput(attrs={"class": 'r-client-info','placeholder': 'UserName', 'autocomplete': 'off','pattern':'[A-Za-z ]+', 'title':'Enter Characters Only '}))
    email = forms.CharField(label='',
                    widget=forms.EmailInput(attrs={"class": 'r-client-info','placeholder': 'Email'}))
    password1 = forms.CharField(label='',
                    widget=forms.PasswordInput(attrs={"class": 'r-client-info','placeholder': 'Password'}))
    password2 = forms.CharField(label='',
                    widget=forms.PasswordInput(attrs={"class": 'r-client-info','placeholder': 'Confirm Password'}))

class UserUpdateForm(UserChangeForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    first_name = forms.CharField(label='',
                    widget=forms.TextInput(attrs={"class": 'r-client-info','placeholder': 'First Name', 'autocomplete': 'off','pattern':'[A-Za-z ]+', 'title':'Enter Characters Only '}))
    
    last_name = forms.CharField(label='',
                    widget=forms.TextInput(attrs={"class": 'r-client-info','placeholder': 'Last Name', 'autocomplete': 'off','pattern':'[A-Za-z ]+', 'title':'Enter Characters Only '}))

    email = forms.CharField(label='',
                    widget=forms.EmailInput(attrs={"class": 'r-client-info','placeholder': 'Email'}))