from django.contrib import admin
from django.urls import path, include
from users import views as users_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('barbershop.urls')),
    path('register/', users_views.register, name='register'),
    path('', include('photocrop.urls')),
    path('', include('services.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
