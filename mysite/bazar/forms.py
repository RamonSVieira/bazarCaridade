from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.forms.widgets import SelectDateWidget
from datetime import datetime

from .models import Usuario, Evento

class UsuarioCadastroForm(forms.Form):
    nome = forms.CharField(max_length=255, required=False)
    email = forms.EmailField(required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].help_text = None
            self.fields[field].label = None
            self.fields[field].error_messages = {'required': None}

class LoginForm(forms.Form):
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

class EventoForm(forms.ModelForm):
    nome = forms.CharField(label='Nome', required=True)
    inicio_display = forms.DateTimeField(label='Início', disabled=True, required=False)
    fim = forms.DateTimeField(label='Fim', required=False, widget=forms.SelectDateWidget())

    class Meta:
        model = Evento
        fields = ['nome', 'inicio_display', 'fim']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['inicio_display'].initial = datetime.now()

    def clean_inicio_display(self):
        return self.fields['inicio_display'].initial