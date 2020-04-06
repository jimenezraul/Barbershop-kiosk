from django.contrib import admin
from .models import Client, Barbers, ZipCode, CompletedClients, LogoImage

admin.site.register(Client)
admin.site.register(Barbers)
admin.site.register(ZipCode)
admin.site.register(CompletedClients)
admin.site.register(LogoImage)


