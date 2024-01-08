from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.views import View
from .forms import UsuarioCadastroForm
from .services import UsuarioService
from .models import Usuario, Evento
from .forms import LoginForm, EventoForm
from django.http import JsonResponse

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
                return render(request, 'logado.html', {'nome': nome})
            else:
                mensagem_erro = "Nome de usuário ou senha incorretos."
                return render(request, self.template_name, {'form': form, 'mensagem_erro': mensagem_erro})

        return render(request, self.template_name, {'form': form})
    
def logout_usuario(request):
    logout(request)
    return redirect('bazar:logar')

# EVENTO
@method_decorator(login_required, name='dispatch')
class EventoView(View):
    template_name = 'evento_list.html'

    def get(self, request):
        eventos = Evento.objects.filter(adm=request.user.usuario)
        return render(request, self.template_name, {'eventos': eventos})
    
@method_decorator(login_required, name='dispatch')
class CriarEventoView(View):
    template_name = 'evento_form.html'

    def get(self, request):
        form = EventoForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.adm = request.user.usuario
            evento.save()
            return redirect('bazar:evento_list')
        return render(request, self.template_name, {'form': form})
    
@method_decorator(login_required, name='dispatch')
class EventoUpdateView(View):
    template_name = 'evento_form.html'

    def get(self, request, eventoid):
        evento = get_object_or_404(Evento, id=eventoid, adm=request.user.usuario)
        form = EventoForm(instance=evento)
        return render(request, self.template_name, {'form': form, 'evento': evento})

    def post(self, request, eventoid):
        evento = get_object_or_404(Evento, id=eventoid, adm=request.user.usuario)
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('bazar:evento_list')
        return render(request, self.template_name, {'form': form, 'evento': evento})
    
@method_decorator(login_required, name='dispatch')
class EventoDeleteView(View):

    def post(self, request, eventoid):
        evento = get_object_or_404(Evento, id=eventoid, adm=request.user.usuario)
        evento.delete()
        return JsonResponse({'status': 'ok'})