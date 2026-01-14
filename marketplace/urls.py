"""
URLs do marketplace
Define todas as rotas da aplicação
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import logout_view

app_name = 'marketplace'

urlpatterns = [
    # Páginas públicas
    path('', views.HomeView.as_view(), name='home'),
    path('como-funciona/', views.ComoFuncionaView.as_view(), name='como-funciona'),
    path('contato/', views.ContatoView.as_view(), name='contato'),
    
    # Autenticação
    path('registro/', views.RegistroView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='marketplace/auth/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', logout_view, name='logout'),

    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    
    # Dashboard principal
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # Perfis
    path('perfil/', views.ProfileUpdateView.as_view(), name='profile-update'),
    path('empreendedor/<int:pk>/', views.EmpreendedorDetailView.as_view(), name='empreendedor-detail'),
    
    # Necessidades (Clientes)
    path('necessidades/', views.NecessidadeListView.as_view(), name='necessidade-list'),
    path('necessidade/criar/', views.NecessidadeCreateView.as_view(), name='necessidade-create'),
    path('necessidade/<int:pk>/', views.NecessidadeDetailView.as_view(), name='necessidade-detail'),
    path('necessidade/<int:pk>/editar/', views.NecessidadeUpdateView.as_view(), name='necessidade-update'),
    path('necessidade/<int:pk>/cancelar/', views.NecessidadeCancelView.as_view(), name='necessidade-cancel'),
    
    # Matches (Conexões)
    path('matches/', views.MatchListView.as_view(), name='match-list'),
    path('match/<int:pk>/', views.MatchDetailView.as_view(), name='match-detail'),
    path('match/<int:pk>/atualizar/', views.MatchUpdateView.as_view(), name='match-update'),
    path('match/<int:pk>/responder/', views.MatchResponseView.as_view(), name='match-response'),
    path('match/<int:pk>/mensagem/', views.MatchMessageView.as_view(), name='match-message'),
    
    # Busca
    path('buscar/', views.SearchView.as_view(), name='search'),
    path('empreendedores/', views.EmpreendedorListView.as_view(), name='empreendedor-list'),
    
    # Ações
    path('necessidade/<int:pk>/interessar/', views.CreateMatchView.as_view(), name='create-match'),
]