from django.contrib import admin
from .models import Address, Appointment, Token, SetmoreAPI

admin.site.register(Address)
admin.site.register(Appointment)
admin.site.register(Token)
admin.site.register(SetmoreAPI)