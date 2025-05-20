from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm  # importa o formulário
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

def index_view(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # Redireciona para a homepage ou outra página
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')  # ou 'login'

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login, redirect, etc.
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})

@login_required
def submit_abstract(request):
    return render(request, 'abstract_submission.html')

def submit_abstract(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        institution = request.POST.get('institution')
        position = request.POST.get('position')
        message = request.POST.get('message')
        pdf_file = request.FILES.get('pdf_file')

        # Aqui poderias guardar num modelo, enviar email, ou processar o PDF
        if pdf_file and pdf_file.name.endswith('.pdf'):
            messages.success(request, 'Resumo submetido com sucesso!')
            return redirect('submit')  # ou outro URL nomeado
        else:
            messages.error(request, 'Por favor, submeta um ficheiro PDF válido.')

    return render(request, 'abstract_submission.html')