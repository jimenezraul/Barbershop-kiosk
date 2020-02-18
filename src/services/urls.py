from django.urls import path
from . import views
from django.conf.urls import url, include

urlpatterns = [
    path('<id>/delete_menservice/', views.delete_menservice, name='services-delete_menservice'),
    path('<id>/delete_kidservice/', views.delete_kidservice, name='services-delete_kidservice'),
    path('<id>/delete_otherservice/', views.delete_otherservice, name='services-delete_otherservice'),
    path('<id>/menservice/', views.update_menservices, name='services-menupdate'),
    path('<id>/kidservice/', views.update_kidservices, name='services-kidupdate'),
    path('<id>/otherservice/', views.update_otherservices, name='services-otherupdate'),
    path('new_men_service/', views.new_men_service, name='services-newmen'),
    path('new_kid_service/', views.new_kid_service, name='services-newkid'),
    path('new_other_service/', views.new_other_service, name='services-newother'),
]