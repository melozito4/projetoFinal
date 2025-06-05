from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Review

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este email já está em uso. Por favor, utilize outro.")
        return email

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['originalidade', 'qualidade', 'relevancia', 'clareza', 'comentario', 'decisao']
        widgets = {
            'originalidade': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'qualidade': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'relevancia': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'clareza': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'comentario': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Comentário profissional...'}),
            'decisao': forms.Select(),
        }

    def clean(self):
        cleaned_data = super().clean()
        for field in ['originalidade', 'qualidade', 'relevancia', 'clareza']:
            value = cleaned_data.get(field)
            if value is None:
                self.add_error(field, "Este campo é obrigatório.")
            elif not (1 <= value <= 10):
                self.add_error(field, "O valor deve estar entre 1 e 10.")
        return cleaned_data
