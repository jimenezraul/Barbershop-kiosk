from django.contrib import admin
from .models import Client, Barbers, ZipCode, LogoImage

admin.site.register(Client)
admin.site.register(Barbers)
admin.site.register(ZipCode)
admin.site.register(LogoImage)

