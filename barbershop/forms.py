from django import forms
from photocrop.models import Photo
from PIL import Image
from django.db import models
from . import models
from .models import Client, Barbers, ZipCode, LogoImage
from django.core.files.storage import FileSystemStorage
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.conf import settings


class CreateClient(forms.ModelForm):

    class Meta:
        model = models.Client
        fields = ["name", "barber"]

    name = forms.CharField(label='',
                           widget=forms.TextInput(attrs={"class": 'client-name', 'placeholder': 'Enter Your Name', 'autocomplete': 'off', 'pattern': '[A-Za-z ]+', 'title': 'Enter Characters Only'}))

    # def __init__(self, *args, **kwargs):
    #     super(CreateClient, self).__init__(*args, **kwargs)

    #     choices_none = [(None, 'Select a Barber')]
    #     choices = [(barber.barber, barber.barber)
    #                for barber in Barbers.objects.all()]

    #     self.fields['barber'] = forms.ChoiceField(choices=choices_none + choices)


class UpdateForm(forms.ModelForm):
    class Meta:
        model = models.Client
        fields = ["name", "barber"]


class ZipCodes(forms.ModelForm):
    class Meta:
        model = models.ZipCode
        fields = ["zip_code"]

    zip_code = forms.CharField(max_length=5, min_length=5, label='',
                               widget=forms.TextInput(attrs={"class": 'client-name', 'placeholder': 'Enter Zip Code', 'autocomplete': 'off', 'pattern': '[0-9 ]+', 'title': 'Enter Numbers Only'}))


class NewBarber(forms.ModelForm):
    class Meta:
        model = models.Barbers
        fields = ["barber", "phone", "license_num", "hire_date", "available"]

    barber = forms.CharField(label='',
                             widget=forms.TextInput(attrs={"class": 'client-name', 'placeholder': 'New Barber\'s Name', 'autocomplete': 'off', 'pattern': '[A-Za-z ]+', 'title': 'Enter Characters Only '}))
    phone = forms.CharField(max_length=10, required=False,
                            widget=forms.TextInput(attrs={"class": 'client-name', 'placeholder': 'Phone Number', 'autocomplete': 'off', 'pattern': '[0-9 ]+', 'title': 'Enter Numbers Only '}))
    license_num = forms.CharField(label='', required=False,
                                  widget=forms.TextInput(attrs={"class": 'client-name', 'placeholder': 'License\'s Number', 'autocomplete': 'off', 'pattern': '[A-Za-z0-9 ]+'}))
    hire_date = forms.DateField(required=False,
                                widget=forms.DateInput(
                                    attrs={'placeholder': 'Hire Date'}, format='%m/%d/%Y'),
                                input_formats=('%m/%d/%Y', )
                                )


class ImageUploadForm(forms.ModelForm):

    class Meta:
        model = models.LogoImage
        fields = ['image']

    # barbershop = forms.CharField(label='',required=False,
        # widget=forms.TextInput(attrs={"class": 'client-name','placeholder': 'Barbershop Name', 'autocomplete': 'off','pattern':'[A-Za-z ]+', 'title':'Enter Characters Only'}))
    image = forms.ImageField(label=_('Company Logo'), required=False, error_messages={
                             'invalid': _("Image files only")}, widget=forms.FileInput)


class BarberPhoto(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = models.Barbers
        fields = ('file', 'x', 'y', 'width', 'height')

    def save(self):
        photo = super(BarberPhoto, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((500, 500), Image.ANTIALIAS)
        resized_image.save(photo.file.path)

        return photo
