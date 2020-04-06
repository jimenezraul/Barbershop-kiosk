from django import forms
from django.db import models
from . import models
from django.core.files.storage import FileSystemStorage
from django.utils.translation import gettext as _

class MenServiceForm(forms.ModelForm):
   
    class Meta:
        model = models.MenServices
        fields = ["service","price"]

    service = forms.CharField(label='',
                    widget=forms.TextInput(attrs={'placeholder': 'Service', 'autocomplete': 'off'}))
    
    price = forms.CharField(label='',
                    widget=forms.TextInput(attrs={'placeholder': 'Price', 'autocomplete': 'off'}))

class KidServiceForm(forms.ModelForm):
   
    class Meta:
        model = models.KidServices
        fields = ["service","price"]

    service = forms.CharField(label='',
                    widget=forms.TextInput(attrs={'placeholder': 'Service', 'autocomplete': 'off'}))
    
    price = forms.CharField(label='',
                    widget=forms.TextInput(attrs={'placeholder': 'Price', 'autocomplete': 'off'}))

class OtherServiceForm(forms.ModelForm):
   
    class Meta:
        model = models.OtherServices
        fields = ["service","price"]

    service = forms.CharField(label='',
                    widget=forms.TextInput(attrs={'placeholder': 'Service', 'autocomplete': 'off'}))
    
    price = forms.CharField(label='',
                    widget=forms.TextInput(attrs={'placeholder': 'Price', 'autocomplete': 'off'}))
