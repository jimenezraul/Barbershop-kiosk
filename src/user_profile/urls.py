from django.urls import path
from . import views
from django.conf.urls import url, include

urlpatterns = [
    path('profile/', views.profile, name='user-profile'),
    path('user_address/', views.user_address, name='user-address'),
    path('user_update_info/<id>', views.update_user_info, name='update_user_info'),
    path('barber_status/<id>', views.barber_status, name='barber_status'),
    path('barber_profile/<id>', views.barber_profile, name='barberprofile'),
    path('barber_profile_update/<id>', views.barber_profile_update, name='barberprofileupdate'),
]