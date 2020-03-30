from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from photocrop.forms import PhotoForm
from photocrop.models import Photo
from barbershop.models import LogoImage, Barbers, Client, CompletedClients
from .forms import AddressForm
from .models import Address
from django.contrib import messages
from .forms import UserUpdateForm
from barbershop.forms import NewBarber, BarberPhoto
from django.db.models import Q
from datetime import datetime, date



@login_required(login_url='register')
def profile(request):
    clients = Client.objects.filter(user=request.user)
    address = Address.objects.filter(user=request.user)
    if address.count() == 1:
        address = address[0]
    
    photoform = PhotoForm()
    user = User.objects.filter(username=request.user)[0]
    photos = Photo.objects.filter(user=request.user)
    if photos.count() == 1:
        photos = photos[0]
    context = {
        'user':user,
        'photoform':photoform,
        'photo':photos,
        'title':'Profile',
        'address':address,
        'clients':clients,
        }
    return render(request, 'user_profile/profile.html', context)


@login_required(login_url='register')
def user_address(request):
    address = Address.objects.filter(user=request.user)
    instance = Address.objects.filter(user=request.user)
    if instance.count() == 1:
        instance = Address.objects.filter(user=request.user)[0]
        if request.method == 'POST':
            form = AddressForm(request.POST, instance=instance)
            if form.is_valid:
                form.save()
                messages.success(request, "Your Info was successfully Updated!")
                return redirect('user-profile')
        else:
            form = AddressForm(instance=instance)
    else:
        if request.method == 'POST':
            form = AddressForm(request.POST, request.user)
            if form.is_valid:
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                return redirect('user-profile')
        else:
            form = AddressForm()
    context = {
        'address': address,
        'form':form,
        'title':'Address',
        }
    return render(request, 'user_profile/user_address.html', context)

@login_required(login_url='register')
def update_user_info(request, id):
    instance = User.objects.get(pk=id)
    logo = LogoImage.objects.filter(user=request.user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST or None, instance=instance)
        if form.is_valid():
            instance.save()
            messages.success(request, "Your Info was successfully Updated!")
            return redirect('user-profile')

    form = UserUpdateForm(instance=instance)
    if logo.count() == 1:
        logo = logo[0]
    else:
        logo = None
    
    context={
        'form':form,
        'logo':logo,
    }
    return render(request, "user_profile/update_user_info.html", context)


@login_required(login_url='register')
def barber_profile(request, id):
    barber = Barbers.objects.get(pk=id)
    photoform = BarberPhoto()
    clients = Client.objects.filter(Q(user=request.user))
    clients = clients.filter(Q(barber=barber) | Q(barber='Any'))
    completed = CompletedClients.objects.filter(completed_by=barber).filter(date=datetime.now())
    if not barber.phone:
        area_code = "000"
        first_3_number = "000"
        last_4_number = "0000"
    else:
        area_code = barber.phone[0:3]
        first_3_number = barber.phone[3:6]
        last_4_number = barber.phone[6:]

    form = NewBarber(instance=barber)
    if barber.available == False:
        checkbox = "unchecked"
    else:
        checkbox = "checked"
    context = {
        "barbers":barber,
        "photoform":photoform,
        "clients":clients,
        "form":form,
        'checkbox': checkbox,
        "completed":completed,
        "area_code": area_code,
        "first_3_number":first_3_number,
        "last_4_number":last_4_number,
    }
    return render(request, "user_profile/barber_profile.html", context)

@login_required(login_url='register')
def barber_status(request, id):
    barbers = Barbers.objects.get(pk=id)
    if request.method == 'POST':
        form = NewBarber(request.POST or None, instance=barbers)
        if form.is_valid:
            form.save()
            messages.success(request, "Status Updated!")
            return redirect('barberprofile', id)
        

    form = NewBarber(instance=barbers)
    if barbers.available == False:
        checkbox = "unchecked"
    else:
        checkbox = "checked"
        
    context={
        'form':form,
        'barbers': barbers,
        'checkbox': checkbox,
    }
    return render(request, "user_profile/barber_status.html", context)

@login_required(login_url='register')
def barber_profile_update(request, id):
    barbers = Barbers.objects.get(pk=id)
    if request.method == 'POST':
        form = NewBarber(request.POST or None, instance=barbers)
        if form.is_valid:
            form.save()
            messages.success(request, "Info Updated!")
            return redirect('barbershop-settings')
    
        

    form = NewBarber(instance=barbers)
    number = barbers.phone
    context={
        'form':form,
        'barbers': barbers,
        "number":number,

    }
    return render(request, "user_profile/barber_profile_update.html", context)