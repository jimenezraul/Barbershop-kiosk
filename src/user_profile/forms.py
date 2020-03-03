from django import forms
from django.db import models
from . import models
from .models import Address

class AddressForm(forms.ModelForm):
   
    class Meta:
        model = models.Address
        fields = ["street","city",'state','zip_code']

    street = forms.CharField(label='',
                    widget=forms.TextInput(attrs={"class": 'r-client-info','placeholder': '123 Street', 'autocomplete': 'off', 'title':'Enter Characters Only'}))

    city = forms.CharField(label='',
                    widget=forms.TextInput(attrs={"class": 'r-client-info','placeholder': 'City', 'autocomplete': 'off','pattern':'[A-Za-z ]+', 'title':'Enter Characters Only'}))

    state = forms.CharField(label='',
                    widget=forms.TextInput(attrs={"class": 'r-client-info','placeholder': 'State', 'autocomplete': 'off','pattern':'[A-Za-z ]+', 'title':'Enter Characters Only'}))

    zip_code = forms.CharField(label='',
                    widget=forms.TextInput(attrs={"class": 'r-client-info','placeholder': 'Zip Code', 'autocomplete': 'off','pattern':'[0-9 ]+', 'title':'Enter Characters Only'}))