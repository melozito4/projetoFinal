from django.contrib import admin
from .models import Profile
from .models import SubmissaoResumo
from .models import InscricaoEvento

admin.site.register(Profile)
admin.site.register(SubmissaoResumo)
admin.site.register(InscricaoEvento)
