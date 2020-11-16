from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Address(models.Model):

    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=12, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.street + self.city + self.street

class Appointment(models.Model):

    name = models.CharField(max_length=30)
    date = models.DateField()
    time = models.CharField(max_length=30, blank=True)
    barber = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.name


class Token(models.Model):

    token = models.CharField(max_length=500)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default=1)


class SetmoreAPI(models.Model):

    token_key = models.CharField(max_length=500)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default=1)