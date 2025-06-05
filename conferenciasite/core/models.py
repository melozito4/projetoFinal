from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    TIPO_CHOICES = [
        ('Default', 'Default'),
        ('Avaliador', 'Avaliador'),
        ('Organizador', 'Organizador'),
        # adiciona mais se necessário
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_utilizador = models.CharField(max_length=50, choices=TIPO_CHOICES, default='Default')

    def __str__(self):
        return f"{self.user.username} Profile"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()

class SubmissaoResumo(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    pdf_file = models.FileField(upload_to='resumos/')
    data_submissao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
# models.py
class InscricaoEvento(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # garante 1 inscrição por conta
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    instituicao = models.CharField(max_length=150, blank=True)
    cargo = models.CharField(max_length=100, blank=True)
    tipo_registo = models.CharField(max_length=50)
    nif = models.CharField(max_length=20, blank=True)
    morada = models.TextField(blank=True)
    data_inscricao = models.DateTimeField(auto_now_add=True)

