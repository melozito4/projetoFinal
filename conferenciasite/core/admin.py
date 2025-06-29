from django.contrib import admin
from .models import Profile, SubmissaoResumo, InscricaoEvento, Atribuicao

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo_utilizador')
    search_fields = ('user__username',)

@admin.register(SubmissaoResumo)
class SubmissaoResumoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'data_submissao', 'status_final')
    list_filter = ('status_final',)
    search_fields = ('titulo', 'autor__username')

@admin.register(InscricaoEvento)
class InscricaoEventoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'tipo_registo', 'data_inscricao')
    search_fields = ('nome', 'email')

@admin.register(Atribuicao)
class AtribuicaoAdmin(admin.ModelAdmin):
    list_display = ('resumo', 'avaliador')
    search_fields = ('resumo__titulo', 'avaliador__username')
