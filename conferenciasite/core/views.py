from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import SubmissaoResumo, InscricaoEvento
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .utils import gerar_fatura_pdf
import stripe
from .forms import ReviewForm
from .models import Review

stripe.api_key = settings.STRIPE_SECRET_KEY


def index_view(request):
    inscrito = False
    limite_atingido = False
    total = InscricaoEvento.objects.count()

    if total >= 100:
        limite_atingido = True

    if request.user.is_authenticated:
        inscrito = InscricaoEvento.objects.filter(user=request.user).exists()

    return render(request, 'index.html', {
        'inscrito': inscrito,
        'limite_atingido': limite_atingido
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registro realizado com sucesso! Faça login para continuar.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def submit_abstract(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        institution = request.POST.get('institution')
        position = request.POST.get('position')
        message = request.POST.get('message')
        pdf_file = request.FILES.get('pdf_file')

        if pdf_file and pdf_file.name.endswith('.pdf'):
            SubmissaoResumo.objects.create(
                autor=request.user,
                titulo=full_name,
                conteudo=message,
                pdf_file=pdf_file
            )
            messages.success(request, 'Resumo submetido com sucesso!')
            return redirect('submit')
        else:
            messages.error(request, 'Por favor, submeta um ficheiro PDF válido.')

    return render(request, 'abstract_submission.html')

def is_avaliador(user):
    return user.is_authenticated and user.profile.tipo_utilizador in ["Avaliador", "Organizador"]

@login_required
@user_passes_test(is_avaliador)
def ver_submissoes(request):
    resumos = SubmissaoResumo.objects.all().order_by('-data_submissao')
    return render(request, 'review.html', {'resumos': resumos})

@login_required
def evento_registo_view(request):
    return render(request, 'event_reg.html')

@login_required
@user_passes_test(is_avaliador)
def ver_resumo(request, resumo_id):
    resumo = get_object_or_404(SubmissaoResumo, pk=resumo_id)
    return render(request, 'ver_resumo.html', {'resumo': resumo})

@csrf_exempt
@login_required
def checkout(request):
    if InscricaoEvento.objects.filter(user=request.user).exists():
        messages.error(request, 'Já estás inscrito no evento.')
        return redirect('evento_registo')

    total_inscritos = InscricaoEvento.objects.count()
    if total_inscritos >= 100:
        messages.error(request, 'As inscrições estão encerradas. O limite de vagas foi atingido.')
        return redirect('evento_registo')

    if request.method == 'POST':
        request.session['evento_data'] = {
            'nome': request.POST.get('nome'),
            'email': request.POST.get('email'),
            'telefone': request.POST.get('telefone'),
            'instituicao': request.POST.get('instituicao'),
            'cargo': request.POST.get('cargo'),
            'tipo_registo': request.POST.get('tipo_registo'),
            'nif': request.POST.get('nif'),
            'morada': request.POST.get('morada'),
        }

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'unit_amount': 2000,
                    'product_data': {
                        'name': 'Inscrição no Evento',
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:8000/sucesso/',
            cancel_url='http://127.0.0.1:8000/evento/',
        )
        return redirect(session.url, code=303)

@login_required
def pagamento_sucesso(request):
    evento_data = request.session.pop('evento_data', None)

    if evento_data and not InscricaoEvento.objects.filter(user=request.user).exists():
        inscricao = InscricaoEvento.objects.create(
            user=request.user,
            nome=evento_data['nome'],
            email=evento_data['email'],
            telefone=evento_data['telefone'],
            instituicao=evento_data['instituicao'],
            cargo=evento_data['cargo'],
            tipo_registo=evento_data['tipo_registo'],
            nif=evento_data['nif'],
            morada=evento_data['morada'],
        )

        pdf_buffer = gerar_fatura_pdf(inscricao)

        email = EmailMessage(
            subject='Confirmação de Inscrição - Conference Hub',
            body='Obrigado pela sua inscrição no evento. Em anexo segue a fatura.',
            from_email='conference@example.com',
            to=[evento_data['email']],
        )
        email.attach('fatura_conferencia.pdf', pdf_buffer.getvalue(), 'application/pdf')
        email.send()

    return render(request, 'sucesso.html')


@login_required
@user_passes_test(is_avaliador)
def ver_resumo(request, resumo_id):
    resumo = get_object_or_404(SubmissaoResumo, pk=resumo_id)
    review_existente = Review.objects.filter(resumo=resumo, avaliador=request.user).first()

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review_existente)
        if form.is_valid():
            nova_review = form.save(commit=False)
            nova_review.resumo = resumo
            nova_review.avaliador = request.user
            nova_review.save()
            messages.success(request, 'Avaliação submetida com sucesso.')
            return redirect('ver_resumo', resumo_id=resumo.id)
    else:
        form = ReviewForm(instance=review_existente)

    todas_reviews = Review.objects.filter(resumo=resumo)

    return render(request, 'ver_resumo.html', {
        'resumo': resumo,
        'form': form,
        'todas_reviews': todas_reviews,
        'review_existente': review_existente,
    })
