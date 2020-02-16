from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm

def register(request): 
    """Register a new user.""" 
    if request.method == 'POST':
    # Show blank registration form. 
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect("signup:raulthebarber-home")
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})
