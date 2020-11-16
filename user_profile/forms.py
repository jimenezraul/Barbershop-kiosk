from django import forms
from django.db import models
from . import models
from .models import Address, Appointment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class AddressForm(forms.ModelForm):

    class Meta:
        model = models.Address
        fields = ["street", "city", 'state', 'zip_code']

    street = forms.CharField(label='',
                             widget=forms.TextInput(attrs={"class": 'r-client-info', 'placeholder': '123 Street', 'autocomplete': 'off', 'title': 'Enter Characters Only'}))

    city = forms.CharField(label='',
                           widget=forms.TextInput(attrs={"class": 'r-client-info', 'placeholder': 'City', 'autocomplete': 'off', 'pattern': '[A-Za-z ]+', 'title': 'Enter Characters Only'}))

    state = forms.CharField(label='',
                            widget=forms.TextInput(attrs={"class": 'r-client-info', 'placeholder': 'State', 'autocomplete': 'off', 'pattern': '[A-Za-z ]+', 'title': 'Enter Characters Only'}))

    zip_code = forms.CharField(label='',
                               widget=forms.TextInput(attrs={"class": 'r-client-info', 'placeholder': 'Zip Code', 'autocomplete': 'off', 'pattern': '[0-9 ]+', 'title': 'Enter Characters Only'}))


class UserUpdateForm(UserChangeForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    first_name = forms.CharField(label='',
                                 widget=forms.TextInput(attrs={"class": 'r-client-info', 'placeholder': 'First Name', 'autocomplete': 'off', 'pattern': '[A-Za-z ]+', 'title': 'Enter Characters Only '}))

    last_name = forms.CharField(label='',
                                widget=forms.TextInput(attrs={"class": 'r-client-info', 'placeholder': 'Last Name', 'autocomplete': 'off', 'pattern': '[A-Za-z ]+', 'title': 'Enter Characters Only '}))

    email = forms.CharField(label='',
                            widget=forms.EmailInput(attrs={"class": 'r-client-info', 'placeholder': 'Email'}))


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["name", "date"]

    name = forms.CharField(label='',
                                 widget=forms.TextInput(attrs={"class": 'r-client-info', 'placeholder': 'Customer\'s Name', 'autocomplete': 'off', 'pattern': '[A-Za-z ]+', 'title': 'Enter Characters Only '}))
    
    date =  forms.DateField(label='',required=False,
                                widget=forms.DateInput(
                                    attrs={'placeholder': 'Date'}, format='%Y-%m-%d'),
                                input_formats=('%Y-%m-%d', )
                                )