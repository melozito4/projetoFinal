from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/index/')  # redirecionar para index após registo
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/index/')  # redirecionar para index após login
        else:
            messages.error(request, 'Credenciais inválidas.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


from django.contrib.auth.decorators import login_required

@login_required
def index_view(request):
    return render(request, 'users/index.html')
