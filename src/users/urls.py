from django.urls import path
from . import views
from django.conf.urls import url, include

urlpatterns = [
    path('login_view/', views.login_view, name='login_view'),
    path('logout_view/', views.logout_view, name='logout_view'),
]