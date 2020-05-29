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
        form = forms.MenServiceForm(request.POST, request.user)
        if form.is_valid():
            service = form.cleaned_data['service']
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, f"{service} was added!")
            return redirect('barbershop-settings')
    else:
        return redirect('barbershop-settings')


def new_kid_service(request):
    if request.method == 'POST':
        form = forms.KidServiceForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, f"{service} was successfully added!")
            return redirect('barbershop-settings')
    else:
        return redirect('barbershop-settings')


def new_other_service(request):
    if request.method == 'POST':
        form = forms.OtherServiceForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, f"{service} was successfully added!")
            return redirect('barbershop-settings')
    else:
        return redirect('barbershop-settings')


def update_menservices(request, id):
    instance = MenServices.objects.get(pk=id)

    if request.method == 'POST':
        form = forms.MenServiceForm(request.POST or None, instance=instance)
        if form.is_valid():
            instance.save()
            messages.success(request, f"{instance.service} was Updated!")
            return redirect('barbershop-settings')
    else:
        form = forms.MenServiceForm(instance=instance)
        context = {
            'form': form,
            'title': 'Update',
        }
        return render(request, 'barbershop/service_update.html', context)


def update_kidservices(request, id):
    instance = KidServices.objects.get(pk=id)

    if request.method == 'POST':
        form = forms.KidServiceForm(request.POST or None, instance=instance)
        if form.is_valid():
            instance.save()
            messages.success(request, f"{instance.service} was Updated!")
            return redirect('barbershop-settings')
    else:
        form = forms.KidServiceForm(instance=instance)
        context = {
            'form': form,
            'title': 'Update',
        }
        return render(request, 'barbershop/service_update.html', context)


def update_otherservices(request, id):
    instance = OtherServices.objects.get(pk=id)

    if request.method == 'POST':
        form = forms.OtherServiceForm(request.POST or None, instance=instance)
        if form.is_valid():
            instance.save()
            messages.success(request, f"{instance.service} was Updated!")
            return redirect('barbershop-settings')
    else:
        form = forms.OtherServiceForm(instance=instance)
        context = {
            'form': form,
            'title': 'Update',
        }
        return render(request, 'barbershop/service_update.html', context)


def delete_menservice(request, id):
    instance = MenServices.objects.get(pk=id)
    
    if request.method == 'POST':
        instance.delete()
        messages.success(request, f"{instance.service} was deleted.")
        return redirect('barbershop-settings')


def delete_kidservice(request, id):
    instance = KidServices.objects.get(pk=id)

    if request.method == 'POST':
        instance.delete()
        messages.success(request, f"{instance.service} was deleted.")
        return redirect('barbershop-settings')


def delete_otherservice(request, id):
    instance = OtherServices.objects.get(pk=id)

    if request.method == 'POST':
        instance.delete()
        messages.success(request, f"{instance.service} was deleted.")
        return redirect('barbershop-settings')
