from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from barbershop.models import LogoImage

def register(request): 
    """Register a new user.""" 
    logo = LogoImage.objects.all()
    if logo.count() == 1:
        logo = logo[0]
    else:
        logo = None
    if request.method == 'POST':
    # Show blank registration form. 
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect("signup:raulthebarber-home")
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
        'logo': logo,
    }
    return render(request, 'users/register.html', context)
