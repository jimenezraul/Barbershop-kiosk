from django import forms
from django.db import models
from . import models
from .models import Client, Barbers, ZipCode, CompletedClients, LogoImage
from django.core.files.storage import FileSystemStorage
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

class CreateClient(forms.ModelForm):
   
    class Meta:
        model = models.Client
        fields = ["name","barber"]

    name = forms.CharField(label='',
                    widget=forms.TextInput(attrs={"class": 'client-name','placeholder': 'Please Enter Your Name', 'autocomplete': 'off','pattern':'[A-Za-z ]+', 'title':'Enter Characters Only'}))

    # def __init__(self, *args, **kwargs):
    #     super(CreateClient, self).__init__(*args, **kwargs)

    #     choices_none = [(None, 'Select a Barber')]
    #     choices = [(barber.barber, barber.barber)
    #                for barber in Barbers.objects.all()]

    #     self.fields['barber'] = forms.ChoiceField(choices=choices_none + choices)
        
class UpdateForm(forms.ModelForm):
    class Meta:
        model = models.Client
        fields = ["name","barber"]

class ZipCodes(forms.ModelForm):
    class Meta:
        model = models.ZipCode
        fields = ["zip_code"]

    zip_code = forms.CharField(max_length=5, min_length=5, label='',
                    widget=forms.TextInput(attrs={"class": 'client-name','placeholder': 'Please Enter Zip Code', 'autocomplete': 'off','pattern':'[0-9 ]+', 'title':'Enter Numbers Only'}))

class NewBarber(forms.ModelForm):
    class Meta:
        model = models.Barbers
        fields = ["barber"]

    barber = forms.CharField(label='',
                    widget=forms.TextInput(attrs={"class": 'client-name','placeholder': 'New Barber\'s Name', 'autocomplete': 'off','pattern':'[A-Za-z ]+', 'title':'Enter Characters Only '}))
    

class CompletedForm(forms.ModelForm):
   
    class Meta:
        model = models.CompletedClients
        fields = ["name","barber","date","user"]

class ImageUploadForm(forms.ModelForm):

    class Meta:
        model = models.LogoImage
        fields = ['image']
        
    image = forms.ImageField(label=_('Company Logo'),required=False, error_messages = {'invalid':_("Image files only")}, widget=forms.FileInput)