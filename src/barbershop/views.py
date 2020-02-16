import requests
from django.conf import settings
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Clients, Barbers, ZipCode, CompletedClients, LogoImage
from services.models import MenServices, KidServices, OtherServices
from . import forms
from services import forms as forms2
from django.contrib import messages
import time
from datetime import datetime, date
import asyncio
import logging
from django.views.generic import UpdateView
from django.db import models
from django.views.generic.edit import UpdateView
from decimal import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


_LOGGER = logging.getLogger()

@login_required(login_url='login_view')
def waitinglist(request):
    clients = Clients.objects.filter(user=request.user)
    date_now = [(client.date) for client in clients]
    fmt = '%H:%M'
    wel_message = ''
    try:
        if clients.count() > 0:
            client = clients[0]
            s = str(client.date)
            start_time = datetime.strptime(s, "%H:%M:%S.%f")
            e = str(datetime.now().time())
            end_time = datetime.strptime(e, "%H:%M:%S.%f")
            total_time = end_time - start_time
            estimate_time = datetime.strptime(str(total_time), "%H:%M:%S.%f").strftime(fmt)
            eta = estimate_time
            my_list = list(eta)
            my_list[0] = ""
            final_list = "".join(my_list)
            client_name = client.name
            #wel_message = f'Hi {client_name}, be ready... We will call you soon!'
            if my_list[1] != '0':
                time_display = "Hour"
            else:
                time_display = "Minutes"
        else:
            final_list = '0:00'
            time_display = "Minutes"
    except:
        final_list = '0:00'
        time_display = "Minutes"
    context= {
        'clients': clients,
        'eta': final_list,
        'time_display': time_display,
        'title': "BarberView",
    }
    return render(request, "barbershop/waitinglist.html", context)

@login_required(login_url='login_view')
def waiting(request):
    kid = KidServices.objects.all()
    men = MenServices.objects.all()
    other = OtherServices.objects.all()
    zip = ZipCode.objects.all()
    logo = LogoImage.objects.all()
    """
    total = 0  

    for service in men:
        prices = service.price
        total += prices
    subtotal = total
    tax_rate = Decimal(.06)
    tax = total * tax_rate
    tax = round(tax, 2)
    total = total + tax
    total = round(total, 2)
     """

    if logo.count() == 1:
        logo = logo[0]
    else:
        logo = None

    if zip.count() > 0:
        zip_code = str(zip[0])
        url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&APPID=8e16366457d9058e262706b08183b818'
        zip = zip_code
        r = requests.get(url.format(zip)).json()
        r_list=list(str(r['main']['temp']))
        r_list[2:]=""
        f_temp="".join(r_list)
        city_weather = {
                'city' : r['name'],
                'temperature' : f_temp,
                'humidity' : r['main']['humidity'],
                'description' : r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon'],
            }
    else:
        url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&APPID=8e16366457d9058e262706b08183b818'
        zip = '10001'
        r = requests.get(url.format(zip)).json()
        r_list=list(str(r['main']['temp']))
        r_list[2:]=""
        f_temp="".join(r_list)
        city_weather = {
                'city' : r['name'],
                'temperature' : f_temp,
                'humidity' : r['main']['humidity'],
                'description' : r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon'],
            }
    clients = Clients.objects.all()
    fmt = '%H:%M'
    wel_message = ''
    try:
        if clients.count() > 0:
            client = clients[0]
            s = str(client.date)
            start_time = datetime.strptime(s, "%H:%M:%S.%f")
            e = str(datetime.now().time())
            end_time = datetime.strptime(e, "%H:%M:%S.%f")
            total_time = end_time - start_time
            estimate_time = datetime.strptime(str(total_time), "%H:%M:%S.%f").strftime(fmt)
            eta = estimate_time
            my_list = list(eta)
            my_list[0] = ""
            final_list = "".join(my_list)
            client_name = client.name
            #wel_message = f'Hi {client_name}, be ready... We will call you soon!'
            if my_list[1] != '0':
                time_display = "Hour"
            else:
                time_display = "Minutes"
        else:
            final_list = '0:00'
            time_display = "Minutes"
    except:
        final_list = '0:00'
        time_display = "Minutes"

    context= {
        'kidservices': kid,
        'menservices': men,
        'otherservices': other,
        'city_weather': city_weather,
        'clients': clients,
        'eta': final_list,
        'time_display': time_display,
        'title': "ClientView",
        'logo': logo,

    }
    return render(request, "barbershop/waiting.html", context)

@login_required(login_url='login_view')
def signup(request):
    logo = LogoImage.objects.all()

    if logo.count() == 1:
        logo = logo[0]
    else:
        logo = None

    barberlist = Barbers.objects.all()
    if request.method == 'POST':
        form = forms.CreateClient(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You has been added to the list. Thank You!")
            return redirect('barbershop-signup')
    else:
        form = forms.CreateClient()
        context= {
        'form': form,
        'title': 'SignUp',
        'barberlist': barberlist,
        'logo': logo,
    }
        return render(request, "barbershop/signup.html", context)

@login_required(login_url='login_view')
def delete_client(request, id):
    instance = Clients.objects.get(pk=id)
    
    form = forms.CompletedClients()
    if request.method == 'POST':
        form.name = instance.name
        form.barber = instance.barber
        form.date = date.today()
        form.save()
        instance.delete()
        messages.success(request, f"{form.name} is Completed!")
        return redirect('barbershop-waitinglist')
    else:
        form = instance
        context= {
        'form': form,
        'title': 'Delete'
    }
        return render(request, 'barbershop/delete.html', context)

@login_required(login_url='login_view')
def update(request, id): 
    logo = LogoImage.objects.all()
    if logo.count() == 1:
        logo = logo[0]
    else:
        logo = None
    instance = Clients.objects.get(pk=id)
    if request.method == 'POST':
        form = forms.UpdateForm(request.POST or None, instance=instance)
        if form.is_valid():
            instance.save()
            messages.success(request, "Client was successfully Updated!")
            return redirect('barbershop-waitinglist')
    else:
        form = forms.UpdateForm(instance=instance)
        context= {
        'form': form,
        'title': 'Update Info',
        'logo': logo,
    }
        return render(request, 'barbershop/update.html', context) 

@login_required(login_url='login_view')
def update_client(request):
    clients = Clients.objects.all()
    context= {
        'clients': clients,
        'title': 'Update'
    }
    return render(request, "barbershop/update_client.html", context)

@login_required(login_url='login_view')
def settings(request): 
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
    
    JAN = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=JAN, date__year__lte=this_year, date__month__lte=JAN)
    FEB = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=FEB, date__year__lte=this_year, date__month__lte=FEB)
    MAR = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=MAR, date__year__lte=this_year, date__month__lte=MAR)
    APR = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=APR, date__year__lte=this_year, date__month__lte=APR)
    MAY = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=MAY, date__year__lte=this_year, date__month__lte=MAY)
    JUN = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=JUN, date__year__lte=this_year, date__month__lte=JUN)
    JUL = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=JUL, date__year__lte=this_year, date__month__lte=JUL)
    AUG = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=AUG, date__year__lte=this_year, date__month__lte=AUG)
    SEP = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=SEP, date__year__lte=this_year, date__month__lte=SEP)
    OCT = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=OCT, date__year__lte=this_year, date__month__lte=OCT)
    NOV = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=NOV, date__year__lte=this_year, date__month__lte=NOV)
    DIC = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=DIC, date__year__lte=this_year, date__month__lte=DIC)
    
    completed_clients = CompletedClients.objects.all()

    if completed_clients.count() > 0:
        completed_clients = CompletedClients.objects.filter(date=datetime.now())

    #Database objects
    barbers = Barbers.objects.all()
    zip_code = ZipCode.objects.all()
    menservices = MenServices.objects.all()
    kidservices = KidServices.objects.all()
    otherservices = OtherServices.objects.all()
    logo = LogoImage.objects.all()
    #Forms
    men_form = forms2.MenServiceForm()
    kid_form = forms2.KidServiceForm()
    other_form = forms2.OtherServiceForm()
    form = forms.NewBarber()
    add_zip = forms.ZipCodes()

    if zip_code.count() > 0:
        zip_form = forms.ZipCodes(instance=zip_code[0])
    else:
        zip_form = forms.ZipCodes()

    if logo.count() > 0:
        upload_image = forms.ImageUploadForm(instance=logo[0])
    else:
        upload_image = forms.ImageUploadForm()

    if request.method == 'POST':
        form = forms.NewBarber(request.POST)
        if form.is_valid():
            name = form.cleaned_data['barber']
            form.save()
            messages.success(request, f"{name} was successfully added!")
            return redirect('barbershop-settings')

    context = {
        #forms
        'men_form': men_form,
        'kid_form': kid_form,
        'other_form': other_form,
        'zip_form': zip_form,
        'form': form,
        'upload_image': upload_image,
        #Objects
        'zipcode': zip_code,
        'add_zip': add_zip,
        'menservices': menservices,
        'kidservices': kidservices,
        'otherservices': otherservices,
        'barbers': barbers,
        'logo': logo,
        'title': 'Settings',
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
        'todays_year': this_year,
    }
    
    return render(request, 'barbershop/settings.html', context) 

@login_required(login_url='login_view')
def delete_barber(request, id): 
    instance = Barbers.objects.get(pk=id)
    if request.method == 'POST':
        instance.delete()
        messages.success(request, f"{instance} was successfully deleted from list!")
        return redirect('barbershop-settings')

@login_required(login_url='login_view')
def newbarber(request): 
    if request.method == 'POST':
        form = forms.NewBarber(request.POST)
        barber = form['barber']
        if form.is_valid():
            name = form.cleaned_data['barber']
            form.save()
            messages.success(request, f"{name} was successfully added!")
            return redirect('barbershop-settings')

@login_required(login_url='login_view')
def zipcode(request, id): 
    instance = ZipCode.objects.get(pk=id)
    if request.method == 'POST':
        form = forms.ZipCodes(request.POST or None, instance=instance)
        if form.is_valid():
            instance.save()
            messages.success(request, "Zip Code was successfully Updated!")
            return redirect('barbershop-settings')

@login_required(login_url='login_view')
def add_zip(request): 
    if request.method == 'POST':
        form = forms.ZipCodes(request.POST)
        if form.is_valid():
            zipcode = form.cleaned_data['zip_code']
            form.save()
            messages.success(request, f"Zip Code: {zipcode} was successfully added!")
            return redirect('barbershop-settings')

@login_required(login_url='login_view')
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
    
    JAN = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=JAN, date__year__lte=this_year, date__month__lte=JAN)
    FEB = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=FEB, date__year__lte=this_year, date__month__lte=FEB)
    MAR = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=MAR, date__year__lte=this_year, date__month__lte=MAR)
    APR = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=APR, date__year__lte=this_year, date__month__lte=APR)
    MAY = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=MAY, date__year__lte=this_year, date__month__lte=MAY)
    JUN = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=JUN, date__year__lte=this_year, date__month__lte=JUN)
    JUL = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=JUL, date__year__lte=this_year, date__month__lte=JUL)
    AUG = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=AUG, date__year__lte=this_year, date__month__lte=AUG)
    SEP = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=SEP, date__year__lte=this_year, date__month__lte=SEP)
    OCT = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=OCT, date__year__lte=this_year, date__month__lte=OCT)
    NOV = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=NOV, date__year__lte=this_year, date__month__lte=NOV)
    DIC = CompletedClients.objects.filter(date__year__gte=this_year,date__month__gte=DIC, date__year__lte=this_year, date__month__lte=DIC)
    
    completed_clients = CompletedClients.objects.all()
    
    if completed_clients.count() > 0:
        completed_clients = CompletedClients.objects.filter(date=datetime.now())

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
        'title':'Completed'
    }
    return render(request, 'barbershop/completed.html', context) 

@login_required(login_url='login_view')
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
    
    JAN = CompletedClients.objects.filter(date__year__gte=last_year,date__month__gte=JAN, date__year__lte=last_year, date__month__lte=JAN)
    FEB = CompletedClients.objects.filter(date__year__gte=last_year,date__month__gte=FEB, date__year__lte=last_year, date__month__lte=FEB)
    MAR = CompletedClients.objects.filter(date__year__gte=last_year,date__month__gte=MAR, date__year__lte=last_year, date__month__lte=MAR)
    APR = CompletedClients.objects.filter(date__year__gte=last_year,date__month__gte=APR, date__year__lte=last_year, date__month__lte=APR)
    MAY = CompletedClients.objects.filter(date__year__gte=last_year,date__month__gte=MAY, date__year__lte=last_year, date__month__lte=MAY)
    JUN = CompletedClients.objects.filter(date__year__gte=last_year,date__month__gte=JUN, date__year__lte=last_year, date__month__lte=JUN)
    JUL = CompletedClients.objects.filter(date__year__gte=last_year,date__month__gte=JUL, date__year__lte=last_year, date__month__lte=JUL)
    AUG = CompletedClients.objects.filter(date__year__gte=last_year,date__month__gte=AUG, date__year__lte=last_year, date__month__lte=AUG)
    SEP = CompletedClients.objects.filter(date__year__gte=last_year,date__month__gte=SEP, date__year__lte=last_year, date__month__lte=SEP)
    OCT = CompletedClients.objects.filter(date__year__gte=last_year,date__month__gte=OCT, date__year__lte=last_year, date__month__lte=OCT)
    NOV = CompletedClients.objects.filter(date__year__gte=last_year,date__month__gte=NOV, date__year__lte=last_year, date__month__lte=NOV)
    DIC = CompletedClients.objects.filter(date__year__gte=last_year,date__month__gte=DIC, date__year__lte=last_year, date__month__lte=DIC)
    
    completed_clients = CompletedClients.objects.all()

    if completed_clients.count() > 0:
        completed_clients = CompletedClients.objects.filter(date=datetime.now())
   

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
        'title':'Last_Year'
    }
    return render(request, 'barbershop/completed.html', context)

@login_required(login_url='login_view')
def upload_image(request):
    if request.method == 'POST':
        form = forms.ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Logo Uploaded!")
            return redirect('barbershop-settings')

@login_required(login_url='login_view')
def image_update(request, id): 
    instance = LogoImage.objects.get(pk=id)
    if request.method == 'POST':
        form = forms.ImageUploadForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Logo was Updated!")
            return redirect('barbershop-settings')

@login_required(login_url='login_view')
def jsonlist(request):
    queryset = MenServices.objects.all()
    print(queryset)
    total = 0  
    for service in queryset:
        prices = service.price
        total += prices
    print(f'SubTotal: ${total}')
    tax_rate = Decimal(.06)
    tax = total * tax_rate
    tax = round(tax, 2)
    print(f'Tax: ${tax}')
    total = total + tax
    total = round(total, 2)
    print(f'Total: ${total}')
    
    queryset = serializers.serialize('json', queryset)
    
    return HttpResponse(queryset, content_type="application/json")
    