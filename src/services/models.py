from django.db import models
from django.utils.translation import ugettext as _

class MenServices(models.Model):

    service = models.CharField(max_length=30)
    price= models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.service) + ": $" + str(self.price)

class KidServices(models.Model):

    service = models.CharField(max_length=30)
    price= models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.service) + ": $" + str(self.price)

class OtherServices(models.Model):

    service = models.CharField(max_length=30)
    price= models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.service) + ": $" + str(self.price)
