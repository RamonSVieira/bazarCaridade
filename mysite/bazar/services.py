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
            # Lidere com o caso em que o e-mail já está cadastrado
            raise ValueError("Este e-mail já está cadastrado.")

    
    @staticmethod
    def autenticar_usuario(request, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        # Autentique o usuário
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Login bem-sucedido
            login(request, user)
            return True, user.usuario.nome
        else:
            # Login falhou
            return False, None
