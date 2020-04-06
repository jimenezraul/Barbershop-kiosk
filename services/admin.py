from django.contrib import admin
from .models import MenServices, KidServices, OtherServices

admin.site.register(MenServices)
admin.site.register(KidServices)
admin.site.register(OtherServices)