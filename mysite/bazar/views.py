from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views import View
from .forms import UsuarioCadastroForm
from .services import UsuarioService
from .models import Usuario
from .forms import LoginForm

def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioCadastroForm(request.POST)
        if form.is_valid():

            # PREENCHA TODOS OS CAMPOS
            if not form.cleaned_data['nome'] or not form.cleaned_data['email'] or not form.cleaned_data['password1']:
                mensagem_erro = "Por favor, preencha todos os campos."
                return render(request, 'cadastro.html', {'form': form, 'mensagem_erro': mensagem_erro})
            
            # EMAIL JA CADASTRADO
            email = form.cleaned_data['email']
            if Usuario.objects.filter(usuario__email=email).exists():
                mensagem_erro = "Este e-mail já está cadastrado."
                return render(request, 'cadastro.html', {'form': form, 'mensagem_erro': mensagem_erro})

            # SENHA MAIOR QUE 6 DIGITOS
            if len(form.cleaned_data['password1']) < 6:
                mensagem_erro = "A senha deve ter pelo menos 6 caracteres."
                return render(request, 'cadastro.html', {'form': form, 'mensagem_erro': mensagem_erro})

            # SENHA NAO COINCIDE
            if form.cleaned_data['password1'] != form.cleaned_data['password2']:
                mensagem_erro = "As senhas não coincidem."
                return render(request, 'cadastro.html', {'form': form, 'mensagem_erro': mensagem_erro})

            # DEU CERTO
            usuario = UsuarioService.cadastrar_usuario(
                email=email,
                password=form.cleaned_data['password1'],
                nome=form.cleaned_data['nome'],
            )
            login(request, usuario.usuario)
            return redirect('bazar:logar')
        else:
            # Se o formulário não for válido, continue exibindo o formulário
            return render(request, 'cadastro.html', {'form': form})
    else:
        form = UsuarioCadastroForm()
        return render(request, 'cadastro.html', {'form': form})
    
class LoginView(View):
    template_name = 'login.html'
    
    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            autenticado, nome = UsuarioService.autenticar_usuario(request, form)

            if autenticado:
                # Login bem-sucedido
                return render(request, 'logado.html', {'nome': nome})
            else:
                # Login falhou
                mensagem_erro = "Nome de usuário ou senha incorretos."
                return render(request, self.template_name, {'form': form, 'mensagem_erro': mensagem_erro})

        return render(request, self.template_name, {'form': form})