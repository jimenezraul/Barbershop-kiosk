from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.conf import settings
from phone_field import PhoneField
from datetime import datetime, date, timedelta

class Client(models.Model):
    
    name = models.CharField(max_length=30)
    barber = models.CharField(max_length=30)
    date = models.TimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

class Barbers(models.Model):

    barber = models.CharField(max_length=30)
    file = models.ImageField(upload_to='barber_profile_img/', blank=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    license_num = models.CharField(max_length=10, blank=True)
    hire_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    available = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.barber

    def years_in_shop(self):
        hire = self.hire_date
        todays_date = datetime.now().date()
        return todays_date.year - hire.year - ((todays_date.month, todays_date.day) < (hire.month, hire.day))

class ZipCode(models.Model):
    zip_code = models.CharField(max_length=5, default=10001)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.zip_code

class CompletedClients(models.Model):
    
    name = models.CharField(max_length=30)
    barber = models.CharField(max_length=30)
    date = models.DateField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    completed_by = models.ForeignKey(Barbers, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name


class LogoImage(models.Model):
    
    image = models.ImageField(upload_to='logo_image/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.image.name