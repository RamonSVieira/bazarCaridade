from django.urls import path
from .views import cadastrar_usuario, LoginView

app_name = 'bazar'
urlpatterns = [
    path('cadastro/', cadastrar_usuario, name='cadastrar_usuario'),
    path('logar/', LoginView.as_view(), name='logar'),  # Corrigir o nome aqui
]
