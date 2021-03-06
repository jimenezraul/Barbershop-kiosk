from django.urls import path
from . import views
from django.conf.urls import url, include


urlpatterns = [
    path('', views.home_page, name='barbershop-home'),
    path('waitinglist/', views.waitinglist, name='barbershop-waitinglist'),
    path('waiting/', views.waiting, name='barbershop-waiting'),
    path('signup/', views.signup, name='barbershop-signup'),
    path('<id>/complete/<barber_id>', views.complete_client, name='barbershop-complete'),
    path('<id>/update', views.update, name='barbershop-update'),
    path('update_client/', views.update_client, name='barbershop-update_client'),
    path('settings/', views.settings, name='barbershop-settings'),
    path('<id>/delete_barber/', views.delete_barber, name='barbershop-delete_barber'),
    path('<id>/zipcode/', views.zipcode, name='barbershop-zipcode'),
    path('addzip/', views.add_zip, name='barbershop-addzip'),
    path('completed/', views.completed, name='barbershop-completed'),
    path('completed/last_year/', views.completed_last_year, name='barbershop-completed_last_year'),
    path('logo/uploaded/', views.upload_image, name='barbershop-upload_image'),
    path('barber_profile_list', views.barber_profile_list, name='barbershop-barberprofilelist'),
    path('logo/uploaded/<id>', views.image_update, name='barbershop-image_update'),
    path('prices/', views.prices, name='barbershop-prices'),

]