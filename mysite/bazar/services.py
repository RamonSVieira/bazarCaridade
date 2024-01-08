from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .models import Usuario

class UsuarioService:
    @staticmethod
    def cadastrar_usuario(email, password, nome):
        User = get_user_model()
        if not User.objects.filter(email=email).exists():
            user = User.objects.create_user(username=email, email=email, password=password)
            usuario = Usuario.objects.create(usuario=user, nome=nome)
            return usuario
        else:
            raise ValueError("Este e-mail já está cadastrado.")

    
    @staticmethod
    def autenticar_usuario(request, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return True, user.usuario.nome
        else:
            return False, None
