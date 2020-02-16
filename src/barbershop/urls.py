from django.urls import path
from . import views
from django.conf.urls import url, include


urlpatterns = [
    path('waitinglist/', views.waitinglist, name='barbershop-waitinglist'),
    path('waiting/', views.waiting, name='barbershop-waiting'),
    path('', views.signup, name='barbershop-signup'),
    path('<id>/delete/', views.delete_client, name='barbershop-delete'),
    path('<id>/update', views.update, name='barbershop-update'),
    path('update_client/', views.update_client, name='barbershop-update_client'),
    path('settings/', views.settings, name='barbershop-settings'),
    path('<id>/delete_barber/', views.delete_barber, name='barbershop-delete_barber'),
    path('newbarber/', views.newbarber, name='barbershop-newbarber'),
    path('<id>/zipcode/', views.zipcode, name='barbershop-zipcode'),
    path('addzip/', views.add_zip, name='barbershop-addzip'),
    path('completed/', views.completed, name='barbershop-completed'),
    path('completed/last_year/', views.completed_last_year, name='barbershop-completed_last_year'),
    path('logo/uploaded/', views.upload_image, name='barbershop-upload_image'),
    path('logo/uploaded/<id>', views.image_update, name='barbershop-image_update'),
    path('json/', views.jsonlist, name='barbershop-json'),
]