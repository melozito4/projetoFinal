from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage

class Profile(models.Model):
    TIPO_CHOICES = [
        ('Default', 'Default'),
        ('Avaliador', 'Avaliador'),
        ('Organizador', 'Organizador'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_utilizador = models.CharField(max_length=50, choices=TIPO_CHOICES, default='Default')
    email_verificado = models.BooleanField(default=False)  # << ADICIONAR ESTA LINHA

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

class InscricaoEvento(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    instituicao = models.CharField(max_length=150, blank=True)
    cargo = models.CharField(max_length=100, blank=True)
    tipo_registo = models.CharField(max_length=50)
    nif = models.CharField(max_length=20, blank=True)
    morada = models.TextField(blank=True)
    data_inscricao = models.DateTimeField(auto_now_add=True)

# Novo modelo para avaliação
class SubmissaoResumo(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aceite', 'Aceite'),
        ('rejeitado', 'Rejeitado'),
    ]

    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    pdf_file = models.FileField(upload_to='resumos/')
    data_submissao = models.DateTimeField(auto_now_add=True)
    status_final = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if self.pk:  # Só verifica alterações se já existir no banco de dados
            original = SubmissaoResumo.objects.get(pk=self.pk)
            if original.status_final != self.status_final:
                # Verificou alteração de status
                assunto = ''
                corpo = ''
                if self.status_final == 'aceite':
                    assunto = 'Resumo Aceite - Conference Hub'
                    corpo = f"""
Caro(a) {self.autor.get_full_name() or self.autor.username},

O seu resumo intitulado "{self.titulo}" foi ACEITE para apresentação na conferência.

Mais informações serão enviadas em breve.

Cumprimentos,
Equipa da Conference Hub
"""
                elif self.status_final == 'rejeitado':
                    assunto = 'Resumo Rejeitado - Conference Hub'
                    corpo = f"""
Caro(a) {self.autor.get_full_name() or self.autor.username},

Após avaliação, o seu resumo intitulado "{self.titulo}" não foi aceite para esta conferência.

Agradecemos a sua participação.

Cumprimentos,
Equipa da Conference Hub
"""
                if assunto and corpo:
                    email = EmailMessage(
                        subject=assunto,
                        body=corpo,
                        from_email='conference@example.com',
                        to=[self.autor.email],
                    )
                    email.send()

        super().save(*args, **kwargs)

class Review(models.Model):
    DECISAO_CHOICES = [
        ('aceite', 'Aceite'),
        ('alteracoes', 'Necessita de alterações'),
        ('rejeitado', 'Rejeitado'),
    ]

    resumo = models.ForeignKey(SubmissaoResumo, on_delete=models.CASCADE, related_name='reviews')
    avaliador = models.ForeignKey(User, on_delete=models.CASCADE)
    originalidade = models.IntegerField()
    qualidade = models.IntegerField()
    relevancia = models.IntegerField()
    clareza = models.IntegerField()
    comentario = models.TextField()
    decisao = models.CharField(max_length=20, choices=DECISAO_CHOICES)
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('resumo', 'avaliador')

    def media(self):
        return round((self.originalidade + self.qualidade + self.relevancia + self.clareza) / 4, 2)

    def __str__(self):
        return f"Review de {self.resumo.titulo} por {self.avaliador.username}"
    
class Atribuicao(models.Model):
    resumo = models.ForeignKey(SubmissaoResumo, on_delete=models.CASCADE, related_name="atribuicoes")
    avaliador = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('resumo', 'avaliador')
        verbose_name = "Atribuição"
        verbose_name_plural = "Atribuições"  # 👈 Corrige o nome plural no admin

    def __str__(self):
        return f"{self.resumo.titulo} → {self.avaliador.username}"