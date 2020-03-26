from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from photocrop.forms import PhotoForm
from photocrop.models import Photo
from barbershop.models import LogoImage
from .forms import AddressForm
from .models import Address
from django.contrib import messages
from .forms import UserUpdateForm
from barbershop.models import Client



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
    print(request.user.id)
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