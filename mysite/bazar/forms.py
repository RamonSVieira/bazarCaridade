from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import Usuario

class UsuarioCadastroForm(forms.Form):
    nome = forms.CharField(max_length=255, required=False)
    email = forms.EmailField(required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remova mensagens específicas
        for field in self.fields:
            self.fields[field].help_text = None  # Remova a ajuda de texto
            self.fields[field].label = None  # Remova o rótulo
            self.fields[field].error_messages = {'required': None}  # Remova a mensagem de campo obrigatório

class LoginForm(forms.Form):
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)