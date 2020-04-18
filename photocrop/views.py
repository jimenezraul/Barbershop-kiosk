from django.shortcuts import render, redirect
from user_profile.urls import *
from .models import Photo
from barbershop.models import Barbers
from .forms import PhotoForm
from django.contrib.auth.models import User
from barbershop.forms import BarberPhoto


def photo_list(request, id=None):
    photos = Photo.objects.filter(user=request.user)
    if photos.count() > 0:
        img_id = photos[0].id
        instance = Photo.objects.get(pk=img_id)
        if request.method == 'POST':
            form = PhotoForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                form.user = instance.user
                form.save()
                return redirect('user-profile')
    else:
        if request.method == 'POST':
            user_id = User.objects.filter(username=request.user)[0].id
            form = PhotoForm(request.POST, request.FILES, request.user)
            if form.is_valid():
                form.save()
                return redirect('user-profile')


def barber_photo(request, id):
    photos = Barbers.objects.filter(pk=id)
    if photos.count() > 0:
        img_id = photos[0].id
        instance = Barbers.objects.get(pk=img_id)
        if request.method == 'POST':
            form = BarberPhoto(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('barberprofile', id)
    else:
        if request.method == 'POST':
            form = BarberPhoto(request.POST, request.FILES, request.user)
            if form.is_valid():
                form.save()
                return redirect('barberprofile', id)
