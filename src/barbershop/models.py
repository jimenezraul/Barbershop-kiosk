from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.conf import settings

class Clients(models.Model):
    
    name = models.CharField(max_length=30)
    barber = models.CharField(max_length=30)
    date = models.TimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

class Barbers(models.Model):

    barber = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.barber

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

    def __str__(self):
        return self.name


class LogoImage(models.Model):
    
    image = models.ImageField(upload_to='logo_image/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

