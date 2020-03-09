from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from barbershop.models import LogoImage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from barbershop.models import LogoImage
from django.contrib.auth.decorators import login_required

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
        'title': "Login - Register",
    }
    return render(request, 'users/register.html', context)

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
        'title': "Login - Register",
    }
    return render(request, "users/register.html", context)

def logout_view(request):
    logout(request)
    return redirect('register')
