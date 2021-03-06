import requests
from photocrop.models import Photo
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Client, Barbers, ZipCode, LogoImage
from services.models import MenServices, KidServices, OtherServices
from . import forms
from services import forms as forms2
from django.contrib import messages
import time
from datetime import datetime, date
import asyncio
import logging
from django.views.generic import UpdateView
from django.views.generic.edit import UpdateView
from decimal import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from photocrop.models import Photo, Gallery
from django.http import HttpResponseRedirect
import json
from .ewt import Estimate


_LOGGER = logging.getLogger()


@login_required(login_url='register')
def waitinglist(request):
    # QS Objects
    photos = Photo.objects.filter(user=request.user)
    barbers = Barbers.objects.filter(user=request.user)
    clients = Client.objects.filter(user=request.user, completed=False)

    if photos.count() == 1:
        photos = photos[0]

    # Estimate Waiting Time
    estimate = Estimate(clients)
    estimate = estimate.get_estimate()
    estimate_time = estimate[0]
    time_display = estimate[1]

    # Pagination
    page = request.GET.get('page', 1)

    paginator = Paginator(clients, 20)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context = {
        'clients': users,
        'eta': estimate_time,
        'time_display': time_display,
        'title': "BarberView",
        'users': users,
        'photos': photos,
        "barbers": barbers,
    }
    return render(request, "barbershop/waitinglist.html", context)


@login_required(login_url='register')
def waiting(request):
    # QS Objects
    kid = KidServices.objects.filter(user=request.user)
    men = MenServices.objects.filter(user=request.user)
    other = OtherServices.objects.filter(user=request.user)
    logo = LogoImage.objects.filter(user=request.user)
    clients = Client.objects.filter(user=request.user, completed=False)

    if logo.count() == 1:
        logo = logo[0]

    # Estimated Wait Time
    try:
        if clients.count() > 0:
            fmt = '%H:%M'
            client = clients[0]
            start_time = str(client.date)
            start_time = datetime.strptime(start_time, "%H:%M:%S.%f")
            end_time = str(datetime.now().time())
            end_time = datetime.strptime(end_time, "%H:%M:%S.%f")
            total_time = end_time - start_time
            estimate_time = datetime.strptime(
                str(total_time), "%H:%M:%S.%f").strftime(fmt)
            estimate_time = estimate_time[1:]
            if estimate_time[0] != '0':
                time_display = "Hour"
            else:
                time_display = "Minutes"
        else:
            estimate_time = '0:00'
            time_display = "Minutes"
    except:
        estimate_time = '0:00'
        time_display = "Minutes"

    # Pagination
    page = request.GET.get('page', 1)

    paginator = Paginator(clients, 20)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context = {
        'kidservices': kid,
        'menservices': men,
        'otherservices': other,
        'clients': users,
        'eta': estimate_time,
        'time_display': time_display,
        'title': "ClientView",
        'logo': logo,
        'users': users,

    }
    return render(request, "barbershop/waiting.html", context)


@login_required(login_url='register')
def signup(request):

    # QS Objects
    client = Client.objects.filter(user=request.user)
    barberlist = Barbers.objects.filter(user=request.user)

    if request.method == 'POST':
        if str(request.user) == "Demo":
            if client.count() == 5:
                messages.success(
                    request, "You have reached the Client's limit of the Demo Account")
                return redirect('barbershop-signup')
            else:
                form = forms.CreateClient(request.POST, request.user)
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.user = request.user
                    instance.save()
                    messages.success(
                        request, "You has been added to the list. Thank You!")
                    return redirect('barbershop-signup')
        else:
            form = forms.CreateClient(request.POST, request.user)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                messages.success(
                    request, "You has been added to the list. Thank You!")
                return redirect('barbershop-signup')
    else:
        form = forms.CreateClient()
        context = {
            'form': form,
            'title': 'SignUp',
            'barberlist': barberlist,
        }
        return render(request, "barbershop/signup.html", context)


@login_required(login_url='register')
def complete_client(request, id, barber_id):

    # QS Objects
    instance = Client.objects.get(pk=id)
    barber = Barbers.objects.get(pk=barber_id)

    if request.method == 'POST':
        instance.completed = True
        instance.completed_by = barber
        instance.status = "Completed"
        instance.date_completed = date.today()
        instance.completed_time = datetime.now().strftime("%I:%M %p")
        instance.save()
        messages.success(request, f"{instance.name} is Completed!")
        try:
            return redirect('barberprofile', barber.id)
        except:
            return redirect('barbershop-waitinglist')
    else:
        form = instance
        context = {
            'form': form,
            'title': 'Delete',
            "barber": barber,
        }
        return render(request, 'barbershop/delete.html', context)


@login_required(login_url='register')
def update(request, id):
    # Instance Client
    instance = Client.objects.get(pk=id)

    if request.method == 'POST':
        form = forms.UpdateForm(request.POST or None, instance=instance)
        if form.is_valid():
            instance.save()
            messages.success(request, "Client was successfully Updated!")
            return redirect('barbershop-waitinglist')
    else:
        form = forms.UpdateForm(instance=instance)
        context = {
            'form': form,
            'title': 'Update Info',
        }
        return render(request, 'barbershop/update.html', context)


@login_required(login_url='register')
def update_client(request):
    # QS Objecst
    clients = Client.objects.all()

    context = {
        'clients': clients,
        'title': 'Update'
    }
    return render(request, "barbershop/update_client.html", context)


@login_required(login_url='register')
def settings(request):
    # QS objects
    barbers = Barbers.objects.filter(user=request.user)
    zip_code = ZipCode.objects.filter(user=request.user)
    menservices = MenServices.objects.filter(user=request.user)
    kidservices = KidServices.objects.filter(user=request.user)
    otherservices = OtherServices.objects.filter(user=request.user)
    logo = LogoImage.objects.filter(user=request.user)
    photos = Photo.objects.filter(user=request.user)
    client = Client.objects.filter(user=request.user)

    # Forms
    men_form = forms2.MenServiceForm()
    kid_form = forms2.KidServiceForm()
    other_form = forms2.OtherServiceForm()
    form = forms.NewBarber()
    add_zip = forms.ZipCodes()

    # Select the first picture in the queryset
    if photos.count() == 1:
        photos = photos[0]

    if zip_code.count() > 0:
        zip_form = forms.ZipCodes(instance=zip_code[0])
    else:
        zip_form = add_zip

    if logo.count() > 0:
        upload_image = forms.ImageUploadForm(instance=logo[0])
    else:
        upload_image = forms.ImageUploadForm()

    if request.method == 'POST':
        if str(request.user) == "Demo":
            if barbers.count() == 5:
                messages.success(
                    request, "You have reached the Barber's limit of the Demo Account")
                return redirect('barbershop-settings')
            else:
                form = forms.NewBarber(request.POST)
                if form.is_valid():
                    name = form.cleaned_data['barber']
                    instance = form.save(commit=False)
                    instance.user = request.user
                    instance.save()
                    messages.success(
                        request, f"{name} was successfully added!")
                    return redirect('barbershop-settings')
        else:
            form = forms.NewBarber(request.POST)
            if form.is_valid():
                name = form.cleaned_data['barber']
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                messages.success(request, f"{name} was successfully added!")
                return redirect('barbershop-settings')

    context = {
        # forms
        'men_form': men_form,
        'kid_form': kid_form,
        'other_form': other_form,
        'zip_form': zip_form,
        'form': form,
        'upload_image': upload_image,
        # Objects
        'zipcode': zip_code,
        'add_zip': add_zip,
        'menservices': menservices,
        'kidservices': kidservices,
        'otherservices': otherservices,
        'barbers': barbers,
        'logo': logo,
        'title': 'Settings',
        'photos': photos,
    }

    return render(request, 'barbershop/settings.html', context)


@login_required(login_url='register')
def delete_barber(request, id):
    instance = Barbers.objects.get(pk=id)
    print("Hello Raul")
    if request.method == 'POST':
        instance.delete()
        messages.success(
            request, f"{instance} was successfully deleted from list!")
        return redirect('barbershop-settings')


@login_required(login_url='register')
def zipcode(request, id):
    instance = ZipCode.objects.get(pk=id)

    if request.method == 'POST':
        form = forms.ZipCodes(request.POST or None, instance=instance)
        if form.is_valid():
            instance.save()
            messages.success(request, "Zip Code was Updated!")
            return redirect('barbershop-settings')


@login_required(login_url='register')
def add_zip(request):
    if request.method == 'POST':
        form = forms.ZipCodes(request.POST, request.user)
        if form.is_valid():
            zipcode = form.cleaned_data['zip_code']
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(
                request, f"Zip Code: {zipcode} was successfully added!")
            return redirect('barbershop-settings')


@login_required(login_url='register')
def completed(request):

    this_year = date.today().year
    last_year = this_year - 1

    JAN = 1
    FEB = 2
    MAR = 3
    APR = 4
    MAY = 5
    JUN = 6
    JUL = 7
    AUG = 8
    SEP = 9
    OCT = 10
    NOV = 11
    DIC = 12

    JAN = Client.objects.filter(
        date_completed__year__gte=this_year, date_completed__month__gte=JAN, date_completed__year__lte=this_year, date_completed__month__lte=JAN, user=request.user, completed=True)
    FEB = Client.objects.filter(
        date_completed__year__gte=this_year, date_completed__month__gte=FEB, date_completed__year__lte=this_year, date_completed__month__lte=FEB, user=request.user, completed=True)
    MAR = Client.objects.filter(
        date_completed__year__gte=this_year, date_completed__month__gte=MAR, date_completed__year__lte=this_year, date_completed__month__lte=MAR, user=request.user, completed=True)
    APR = Client.objects.filter(
        date_completed__year__gte=this_year, date_completed__month__gte=APR, date_completed__year__lte=this_year, date_completed__month__lte=APR, user=request.user, completed=True)
    MAY = Client.objects.filter(
        date_completed__year__gte=this_year, date_completed__month__gte=MAY, date_completed__year__lte=this_year, date_completed__month__lte=MAY, user=request.user, completed=True)
    JUN = Client.objects.filter(
        date_completed__year__gte=this_year, date_completed__month__gte=JUN, date_completed__year__lte=this_year, date_completed__month__lte=JUN, user=request.user, completed=True)
    JUL = Client.objects.filter(
        date_completed__year__gte=this_year, date_completed__month__gte=JUL, date_completed__year__lte=this_year, date_completed__month__lte=JUL, user=request.user, completed=True)
    AUG = Client.objects.filter(
        date_completed__year__gte=this_year, date_completed__month__gte=AUG, date_completed__year__lte=this_year, date_completed__month__lte=AUG, user=request.user, completed=True)
    SEP = Client.objects.filter(
        date_completed__year__gte=this_year, date_completed__month__gte=SEP, date_completed__year__lte=this_year, date_completed__month__lte=SEP, user=request.user, completed=True)
    OCT = Client.objects.filter(
        date_completed__year__gte=this_year, date_completed__month__gte=OCT, date_completed__year__lte=this_year, date_completed__month__lte=OCT, user=request.user, completed=True)
    NOV = Client.objects.filter(
        date_completed__year__gte=this_year, date_completed__month__gte=NOV, date_completed__year__lte=this_year, date_completed__month__lte=NOV, user=request.user, completed=True)
    DIC = Client.objects.filter(
        date_completed__year__gte=this_year, date_completed__month__gte=DIC, date_completed__year__lte=this_year, date_completed__month__lte=DIC, user=request.user, completed=True)

    completed_clients = Client.objects.filter(
        user=request.user, completed=True)

    if completed_clients.count() > 0:
        completed_clients = Client.objects.filter(user=request.user,
                                                  date=datetime.now())

    page = request.GET.get('page', 1)
    paginator = Paginator(completed_clients, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context = {
        'todays_year': this_year,
        'last_year': last_year,
        'completed': users,
        'JAN': JAN,
        'FEB': FEB,
        'MAR': MAR,
        'APR': APR,
        'MAY': MAY,
        'JUN': JUN,
        'JUL': JUL,
        'AUG': AUG,
        'SEP': SEP,
        'OCT': OCT,
        'NOV': NOV,
        'DIC': DIC,
        'title': 'Completed',
        'users': users,
    }
    return render(request, 'barbershop/completed.html', context)


@login_required(login_url='register')
def completed_last_year(request):

    this_year = date.today().year
    last_year = this_year - 1

    JAN = 1
    FEB = 2
    MAR = 3
    APR = 4
    MAY = 5
    JUN = 6
    JUL = 7
    AUG = 8
    SEP = 9
    OCT = 10
    NOV = 11
    DIC = 12

    JAN = Client.objects.filter(
        date_completed__year__gte=last_year, date_completed__month__gte=JAN, date_completed__year__lte=last_year, date_completed__month__lte=JAN, user=request.user)
    FEB = Client.objects.filter(
        date_completed__year__gte=last_year, date_completed__month__gte=FEB, date_completed__year__lte=last_year, date_completed__month__lte=FEB, user=request.user)
    MAR = Client.objects.filter(
        date_completed__year__gte=last_year, date_completed__month__gte=MAR, date_completed__year__lte=last_year, date_completed__month__lte=MAR, user=request.user)
    APR = Client.objects.filter(
        date_completed__year__gte=last_year, date_completed__month__gte=APR, date_completed__year__lte=last_year, date_completed__month__lte=APR, user=request.user)
    MAY = Client.objects.filter(
        date_completed__year__gte=last_year, date_completed__month__gte=MAY, date_completed__year__lte=last_year, date_completed__month__lte=MAY, user=request.user)
    JUN = Client.objects.filter(
        date_completed__year__gte=last_year, date_completed__month__gte=JUN, date_completed__year__lte=last_year, date_completed__month__lte=JUN, user=request.user)
    JUL = Client.objects.filter(
        date_completed__year__gte=last_year, date_completed__month__gte=JUL, date_completed__year__lte=last_year, date_completed__month__lte=JUL, user=request.user)
    AUG = Client.objects.filter(
        date_completed__year__gte=last_year, date_completed__month__gte=AUG, date_completed__year__lte=last_year, date_completed__month__lte=AUG, user=request.user)
    SEP = Client.objects.filter(
        date_completed__year__gte=last_year, date_completed__month__gte=SEP, date_completed__year__lte=last_year, date_completed__month__lte=SEP, user=request.user)
    OCT = Client.objects.filter(
        date_completed__year__gte=last_year, date_completed__month__gte=OCT, date_completed__year__lte=last_year, date_completed__month__lte=OCT, user=request.user)
    NOV = Client.objects.filter(
        date_completed__year__gte=last_year, date_completed__month__gte=NOV, date_completed__year__lte=last_year, date_completed__month__lte=NOV, user=request.user)
    DIC = Client.objects.filter(
        date_completed__year__gte=last_year, date_completed__month__gte=DIC, date_completed__year__lte=last_year, date_completed__month__lte=DIC, user=request.user)

    completed_clients = Client.objects.filter(user=request.user)

    if completed_clients.count() > 0:
        completed_clients = Client.objects.filter(user=request.user,
                                                  date=datetime.now())

    context = {
        'todays_year': this_year,
        'last_year': last_year,
        'completed': completed_clients,
        'JAN': JAN,
        'FEB': FEB,
        'MAR': MAR,
        'APR': APR,
        'MAY': MAY,
        'JUN': JUN,
        'JUL': JUL,
        'AUG': AUG,
        'SEP': SEP,
        'OCT': OCT,
        'NOV': NOV,
        'DIC': DIC,
        'title': 'Last_Year'
    }
    return render(request, 'barbershop/completed.html', context)


@login_required(login_url='register')
def upload_image(request):
    if request.method == 'POST':
        form = forms.ImageUploadForm(request.POST, request.FILES, request.user)
        if form.is_valid():
            form.user = request.user
            form.save()
            messages.success(request, "Logo Uploaded!")
            return redirect('barbershop-settings')


@login_required(login_url='register')
def image_update(request, id):
    instance = LogoImage.objects.get(pk=id)

    if request.method == 'POST':
        form = forms.ImageUploadForm(
            request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Logo was Updated!")
            return redirect('barbershop-settings')


@login_required(login_url='register')
def barber_profile_list(request):
    # QS Objects
    barbers = Barbers.objects.filter(user=request.user)

    # Form
    form = forms.NewBarber()

    if request.method == 'POST':
        form = forms.NewBarber(request.POST)
        if form.is_valid():
            name = form.cleaned_data['barber']
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, f"{name} was successfully added!")
            return redirect('barbershop-barberprolist')
    
    context = {
        "barbers": barbers,
        "form": form,
    }
    return render(request, "barbershop/barber_profile_list.html", context)


@login_required(login_url='register')
def home_page(request):
    return render(request, "barbershop/home.html")


@login_required(login_url='register')
def prices(request):
    # QS Objects
    logo = LogoImage.objects.filter(user=request.user)
    galleries = Gallery.objects.filter(user=request.user)

    if galleries.count() > 0:
        galleries = galleries[0:4]
    else:
        galleries = None

    if logo.count() > 0:
        logo = logo[0]
    else:
        logo = None

    men_service = MenServices.objects.filter(user=request.user)
    men_service = men_service[0:4]
    kid_service = KidServices.objects.filter(user=request.user)
    kid_service = kid_service[0:4]
    other_service = OtherServices.objects.filter(user=request.user)
    other_service = other_service[0:4]
    context = {
        "logo": logo,
        "men": men_service,
        "kid": kid_service,
        "other": other_service,
        "galleries": galleries,
    }
    return render(request, "barbershop/prices_menu.html", context)
