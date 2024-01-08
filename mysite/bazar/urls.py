from django.urls import path
from . import views

app_name = 'bazar'
urlpatterns = [
    path('cadastro/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('logar/', views.LoginView.as_view(), name='logar'),
    path('logout/', views.logout_usuario, name='logout'),

    path('eventos/', views.EventoView.as_view(), name='evento_list'),
    path('eventos/cadastrar/', views.CriarEventoView.as_view(), name='evento_create'),
    path('evento/update/<int:eventoid>/', views.EventoUpdateView.as_view(), name='evento_update'),
    path('eventos/<int:eventoid>/deletar/', views.EventoDeleteView.as_view(), name='evento_delete'),
]
