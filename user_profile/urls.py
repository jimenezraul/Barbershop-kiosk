from django.urls import path
from . import views
from django.conf.urls import url, include

urlpatterns = [
    path('profile/', views.profile, name='user-profile'),
    path('user_address/', views.user_address, name='user-address'),
    path('user_update_info/<id>', views.update_user_info, name='update_user_info'),
    path('barber_status/<id>', views.barber_status, name='barber_status'),
    path('update_token/<id>', views.update_token, name='update-token'),
    path('barber_profile/<id>', views.barber_profile, name='barberprofile'),
    path('barber_profile_update/<id>', views.barber_profile_update, name='barberprofileupdate'),
    path('barber_create_appointment/<id>/<time>', views.create_appointment, name='barber-create-appointment'),
    path('appointment/<id>/<time>', views.appointment, name='appointment'),
    path('appointment_services/<id>/', views.appointment_services, name='appointment-services'),
    path('appointment_slots/<id>/<staff_key>/<service_key>/', views.appointment_slots, name='appointment-slots'),
    path('appointment_date/<id>/<staff_key>/<service_key>/', views.appointment_date, name='appointment-date'),
]