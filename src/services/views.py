from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import MenServices, KidServices, OtherServices
from barbershop.models import LogoImage
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from barbershop.models import LogoImage



def new_men_service(request): 
    if request.method == 'POST':
        form = forms.MenServiceForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            form.save()
            messages.success(request, f"{service} was successfully added!")
            return redirect('barbershop-settings')
    else:
        return redirect('barbershop-settings')

def new_kid_service(request): 
    if request.method == 'POST':
        form = forms.KidServiceForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            form.save()
            messages.success(request, f"{service} was successfully added!")
            return redirect('barbershop-settings')
    else:
        return redirect('barbershop-settings')

def new_other_service(request): 
    if request.method == 'POST':
        form = forms.OtherServiceForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            form.save()
            messages.success(request, f"{service} was successfully added!")
            return redirect('barbershop-settings')
    else:
        return redirect('barbershop-settings')
        
def update_menservices(request, id): 
    logo = LogoImage.objects.all()

    if logo.count() == 1:
        logo = logo[0]
    else:
        logo = None

    instance = MenServices.objects.get(pk=id)
    if request.method == 'POST':
        form = forms.MenServiceForm(request.POST or None, instance=instance)
        if form.is_valid():
            instance.save()
            messages.success(request, f"{instance} was successfully Updated!")
            return redirect('barbershop-settings')
    else:
        form = forms.MenServiceForm(instance=instance)
        context= {
        'form': form,
        'title': 'Update',
        'logo': logo,
    }
        return render(request, 'barbershop/service_update.html', context)

def update_kidservices(request, id): 
    logo = LogoImage.objects.all()

    if logo.count() == 1:
        logo = logo[0]
    else:
        logo = None

    instance = KidServices.objects.get(pk=id)
    if request.method == 'POST':
        form = forms.KidServiceForm(request.POST or None, instance=instance)
        if form.is_valid():
            instance.save()
            messages.success(request, f"{instance} was successfully Updated!")
            return redirect('barbershop-settings')
    else:
        form = forms.KidServiceForm(instance=instance)
        context= {
        'form': form,
        'title': 'Update',
        'logo': logo,
    }
        return render(request, 'barbershop/service_update.html', context)

def update_otherservices(request, id): 
    logo = LogoImage.objects.all()
    
    if logo.count() == 1:
        logo = logo[0]
    else:
        logo = None
        
    instance = OtherServices.objects.get(pk=id)
    if request.method == 'POST':
        form = forms.OtherServiceForm(request.POST or None, instance=instance)
        if form.is_valid():
            instance.save()
            messages.success(request, f"{instance} was successfully Updated!")
            return redirect('barbershop-settings')
    else:
        form = forms.OtherServiceForm(instance=instance)
        context= {
        'form': form,
        'title': 'Update',
        'logo': logo,
    }
        return render(request, 'barbershop/service_update.html', context)

def delete_menservice(request, id): 
    instance = MenServices.objects.get(pk=id)
    if request.method == 'POST':
        instance.delete()
        messages.success(request, f"{instance} was successfully deleted from list!")
        return redirect('barbershop-settings')

def delete_kidservice(request, id): 
    instance = KidServices.objects.get(pk=id)
    if request.method == 'POST':
        instance.delete()
        messages.success(request, f"{instance} was successfully deleted from list!")
        return redirect('barbershop-settings')

def delete_otherservice(request, id): 
    instance = OtherServices.objects.get(pk=id)
    if request.method == 'POST':
        instance.delete()
        messages.success(request, f"{instance} was successfully deleted from list!")
        return redirect('barbershop-settings')

def login_view(request):
    logo = LogoImage.objects.all()
    if logo.count() == 1:
        logo = logo[0]
    else:
        logo = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        try:
            if user is not None:
                if 'next' in request.POST:
                    login(request, user)
                    return redirect(request.POST.get('next'))
                else:
                    login(request, user)
                    return redirect('barbershop-waitinglist')
            else:
                messages.error(request,'username or password is not correct')
                return redirect(request.POST.get('next'))
        except:
            return redirect('barbershop-waitinglist')
    context= {
        'logo': logo,
    }
    return render(request, "users/login.html", context)

def logout_view(request):
    logout(request)
    return redirect('login_view')