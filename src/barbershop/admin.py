from django.contrib import admin
from .models import Clients, Barbers, ZipCode, CompletedClients, LogoImage

admin.site.register(Clients)
admin.site.register(Barbers)
admin.site.register(ZipCode)
admin.site.register(CompletedClients)
admin.site.register(LogoImage)


