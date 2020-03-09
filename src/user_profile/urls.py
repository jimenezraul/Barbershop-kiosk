from django.urls import path
from . import views
from django.conf.urls import url, include

urlpatterns = [
    path('profile/', views.profile, name='user-profile'),
    path('user_address/', views.user_address, name='user-address'),
    path('user_update_info/<id>', views.update_user_info, name='update_user_info'),
]