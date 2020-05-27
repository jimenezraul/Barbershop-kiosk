from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.conf import settings
from phone_field import PhoneField
from datetime import datetime, date, timedelta
from django.urls import reverse


class Barbers(models.Model):

    barber = models.CharField(max_length=30)
    file = models.ImageField(upload_to='barber_profile_img/', blank=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    license_num = models.CharField(max_length=10, blank=True)
    hire_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True)
    available = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.barber

    def years_in_shop(self):
        hire = self.hire_date
        todays_date = datetime.now().date()
        return todays_date.year - hire.year - ((todays_date.month, todays_date.day) < (hire.month, hire.day))
    
    def save(self, *args, **kwargs):
        try:
            photo = Barbers.objects.get(id=self.id)
            if photo.file != self.file:
                photo.file.delete()
        except: pass
        super(Barbers, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        photo = Barbers.objects.get(id=self.id)
        photo.file.delete()
        return super(Barbers, self).delete(*args, **kwargs)

    @property
    def object_delete(self):
        return f"/{self.pk}/delete_barber/"


class Client(models.Model):
    WAITING = 'Waiting'
    SERVING = 'Serving'
    COMPLETED = 'Completed'

    STATUS_CHOICES = [
        (WAITING, 'Waiting'),
        (SERVING, 'Serving'),
        (COMPLETED, 'Completed'),
    ]
    name = models.CharField(max_length=30)
    barber = models.CharField(max_length=30)
    date = models.TimeField(auto_now_add=True)
    date_completed = models.DateField(max_length=30, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default=1)
    completed = models.BooleanField(default=False)
    completed_by = models.ForeignKey(
        Barbers, on_delete=models.CASCADE, blank=True, null=True)
    completed_time = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=WAITING,
    )
    

    def __str__(self):
        return self.name


class ZipCode(models.Model):
    zip_code = models.CharField(max_length=5, default=10001)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.zip_code


class LogoImage(models.Model):

    file = models.ImageField(upload_to='logo_image/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.file.name

    def save(self, *args, **kwargs):
        try:
            photo = LogoImage.objects.get(id=self.id)
            if photo.file != self.file:
                photo.file.delete()
        except: pass
        super(LogoImage, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        photo = LogoImage.objects.get(id=self.id)
        photo.file.delete()
        super(LogoImage, self).save(*args, **kwargs)