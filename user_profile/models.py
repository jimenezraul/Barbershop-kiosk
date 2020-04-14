from django.db import models
from django.conf import settings


class Address(models.Model):

    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=12, default='32738')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.street + self.city + self.street
