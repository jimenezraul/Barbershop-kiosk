from django.db import models
from django.conf import settings

class MenServices(models.Model):

    service = models.CharField(max_length=30)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

    def __str__(self):
        return str(self.service) + ": $" + str(self.price)

class KidServices(models.Model):

    service = models.CharField(max_length=30)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

    def __str__(self):
        return str(self.service) + ": $" + str(self.price)

class OtherServices(models.Model):

    service = models.CharField(max_length=30)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    
    def __str__(self):
        return str(self.service) + ": $" + str(self.price)
