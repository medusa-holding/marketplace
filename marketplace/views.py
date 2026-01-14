"""
Views do marketplace
Implementa toda a lógica da aplicação usando Class-Based Views
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    TemplateView, ListView, DetailView, 
    CreateView, UpdateView, DeleteView, View
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone

from .models import (
    User, Empreendedor, Cliente, Category,
    Necessidade, Match, Message
)
from .forms import (
    UserRegistrationForm, EmpreendedorProfileForm,
    ClienteProfileForm, NecessidadeForm, MatchResponseForm,
    MessageForm, SearchForm, ContactForm
)


class HomeView(TemplateView):
    """
    Página inicial do marketplace
    """
    template_name = 'marketplace/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)[:8]
        context['empreendedores_count'] = Empreendedor.objects.filter(is_active=True).count()
        context['necessidades_count'] = Necessidade.objects.filter(status='aberto').count()
        context['matches_count'] = Match.objects.filter(is_active=True).count()
        return context


class ComoFuncionaView(TemplateView):
    """
    Página explicando como funciona a plataforma
    """
    template_name = 'marketplace/como_funciona.html'


class ContatoView(TemplateView):
    """
    Página de contato
    """
    template_name = 'marketplace/contato.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Mensagem enviada com sucesso! Entraremos em contato em breve.')
            return redirect('marketplace:contato')
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class RegistroView(CreateView):
    """
    View de registro de novos usuários
    """
    form_class = UserRegistrationForm
    template_name = 'marketplace/auth/register.html'
    success_url = reverse_lazy('marketplace:dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        # Redireciona usuários autenticados
        if request.user.is_authenticated:
            return redirect('marketplace:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Cria o perfil correspondente
        user = form.instance
        if user.user_type == 'empreendedor':
            Empreendedor.objects.create(user=user)
        else:
            Cliente.objects.create(user=user)
        # Faz login automaticamente
        login(self.request, user)
        messages.success(self.request, 'Conta criada com sucesso!')
        return response


def logout_view(request):
    user = request.user
    logout(request)
    messages.success(request, 'Sessão terminada com sucesso.')
    return redirect('marketplace:login')


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Dashboard principal personalizado por tipo de usuário
    """
    template_name = 'marketplace/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_empreendedor:
            # Dashboard do empreendedor
            empreendedor = user.empreendedor_profile
            context['matches'] = Match.objects.filter(
                empreendedor=empreendedor,
                is_active=True
            ).select_related('necessidade', 'necessidade__cliente').order_by('-date_created')[:10]
            
            context['novos_matches'] = Match.objects.filter(
                empreendedor=empreendedor,
                status='novo'
            ).count()
            
            context['matches_em_conversa'] = Match.objects.filter(
                empreendedor=empreendedor,
                status='em_conversa'
            ).count()
            
            context['matches_fechados'] = Match.objects.filter(
                empreendedor=empreendedor,
                status='fechado'
            ).count()
            
        else:
            # Dashboard do cliente
            cliente = user.cliente_profile
            context['minhas_necessidades'] = Necessidade.objects.filter(
                cliente=cliente
            ).order_by('-date_created')[:10]
            
            context['necessidades_abertas'] = Necessidade.objects.filter(
                cliente=cliente,
                status='aberto'
            ).count()
            
            context['respostas_recebidas'] = Match.objects.filter(
                necessidade__cliente=cliente,
                status__in=['novo', 'visualizado', 'em_conversa']
            ).count()
            
            context['servicos_contratados'] = Match.objects.filter(
                necessidade__cliente=cliente,
                status='fechado'
            ).count()
        
        return context



class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    View para atualizar perfil do usuário
    """
    template_name = 'marketplace/profile_update.html'
    success_url = reverse_lazy('marketplace:dashboard')
    
    def get_object(self):
        user = self.request.user
        if user.is_empreendedor:
            return user.empreendedor_profile
        else:
            return user.cliente_profile
    
    def get_form_class(self):
        if self.request.user.is_empreendedor:
            return EmpreendedorProfileForm
        else:
            return ClienteProfileForm
    
    def form_valid(self, form):
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return super().form_valid(form)


class EmpreendedorListView(ListView):
    """
    Lista de empreendedores cadastrados
    """
    model = Empreendedor
    template_name = 'marketplace/empreendedor_list.html'
    context_object_name = 'empreendedores'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Empreendedor.objects.filter(is_active=True).select_related('category', 'user')
        
        # Filtros
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(business_name__icontains=search) |
                Q(description__icontains=search) |
                Q(services__icontains=search) |
                Q(location__icontains=search)
            )
        
        return queryset.order_by('-is_verified', 'business_name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['search_form'] = SearchForm(self.request.GET)
        return context


class EmpreendedorDetailView(DetailView):
    """
    Detalhes de um empreendedor
    """
    model = Empreendedor
    template_name = 'marketplace/empreendedor_detail.html'
    context_object_name = 'empreendedor'
    
    def get_queryset(self):
        return Empreendedor.objects.filter(is_active=True).select_related('category', 'user')


from django.db.models import Case, When, IntegerField
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Necessidade, Category, Match

class NecessidadeListView(LoginRequiredMixin, ListView):
    """
    Lista de necessidades (para empreendedores verem),
    ordenadas por prioridade de urgência e data de criação.
    """
    model = Necessidade
    template_name = 'marketplace/necessidade_list.html'
    context_object_name = 'necessidades'
    paginate_by = 10
    
    def get_queryset(self):
        # Apenas necessidades abertas
        queryset = Necessidade.objects.filter(
            status='aberto'
        ).select_related('category', 'cliente', 'cliente__user')
        
        # Filtros
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        # Ordenação por urgência (com prioridade numérica) e data de criação
        queryset = queryset.annotate(
            urgency_order=Case(
                When(urgency='urgente', then=4),
                When(urgency='alta', then=3),
                When(urgency='normal', then=2),
                When(urgency='baixa', then=1),
                output_field=IntegerField()
            )
        ).order_by('-urgency_order', '-date_created')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lista de categorias para filtros
        context['categories'] = Category.objects.filter(is_active=True)
        
        # Adiciona contagem de interesses/matches para cada necessidade
        for necessidade in context['necessidades']:
            necessidade.interest_count = Match.objects.filter(
                necessidade=necessidade,
                is_active=True
            ).count()
        
        return context



class NecessidadeDetailView(LoginRequiredMixin, DetailView):
    """
    Detalhes de uma necessidade
    """
    model = Necessidade
    template_name = 'marketplace/necessidade_detail.html'
    context_object_name = 'necessidade'
    
    def get_queryset(self):
        return Necessidade.objects.select_related(
            'category', 'cliente', 'cliente__user'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_empreendedor:
            # Verifica se já existe match
            try:
                context['existing_match'] = Match.objects.get(
                    necessidade=self.object,
                    empreendedor=user.empreendedor_profile
                )
            except Match.DoesNotExist:
                context['existing_match'] = None
        
        return context


class NecessidadeCreateView(LoginRequiredMixin, CreateView):
    """
    Criar nova necessidade (clientes)
    """
    form_class = NecessidadeForm
    template_name = 'marketplace/necessidade_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_empreendedor:
            messages.error(request, 'Apenas clientes podem criar necessidades.')
            return redirect('marketplace:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.cliente = self.request.user.cliente_profile
        response = super().form_valid(form)
        messages.success(self.request, 'Necessidade criada com sucesso!')
        return response


class NecessidadeUpdateView(LoginRequiredMixin, UpdateView):
    """
    Editar necessidade (apenas cliente proprietário)
    """
    model = Necessidade
    form_class = NecessidadeForm
    template_name = 'marketplace/necessidade_form.html'
    
    def get_queryset(self):
        return Necessidade.objects.filter(
            cliente=self.request.user.cliente_profile
        )
    
    def form_valid(self, form):
        messages.success(self.request, 'Necessidade atualizada com sucesso!')
        return super().form_valid(form)


class NecessidadeCancelView(LoginRequiredMixin, View):
    """
    Cancelar uma necessidade
    """
    def post(self, request, pk, *args, **kwargs):
        necessidade = get_object_or_404(
            Necessidade, 
            pk=pk, 
            cliente=request.user.cliente_profile
        )
        necessidade.status = 'cancelado'
        necessidade.save()
        
        # Cancela matches ativos
        Match.objects.filter(
            necessidade=necessidade,
            is_active=True
        ).update(is_active=False)
        
        messages.success(request, 'Necessidade cancelada com sucesso.')
        return redirect('marketplace:dashboard')


class CreateMatchView(LoginRequiredMixin, View):
    """
    Criar match (empreendedor se interessa por uma necessidade)
    """
    def post(self, request, pk, *args, **kwargs):
        if not request.user.is_empreendedor:
            messages.error(request, 'Apenas empreendedores podem se candidatar.')
            return redirect('marketplace:dashboard')
        
        necessidade = get_object_or_404(Necessidade, pk=pk, status='aberto')
        empreendedor = request.user.empreendedor_profile
        
        # Verifica se já existe match
        if Match.objects.filter(
            necessidade=necessidade,
            empreendedor=empreendedor
        ).exists():
            messages.warning(request, 'Você já se candidatou para esta necessidade.')
            return redirect('marketplace:necessidade-detail', pk=pk)
        
        # Cria o match
        Match.objects.create(
            necessidade=necessidade,
            empreendedor=empreendedor,
            status='novo'
        )
        
        messages.success(request, 'Candidatura enviada! Aguarde o contato do cliente.')
        return redirect('marketplace:match-detail', pk=Match.objects.latest('id').id)


class MatchListView(LoginRequiredMixin, ListView):
    template_name = 'marketplace/match_list.html'
    context_object_name = 'matches'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        status = self.request.GET.get('status')

        if user.is_empreendedor:
            qs = Match.objects.filter(
                empreendedor=user.empreendedor_profile,
                is_active=True
            )
        else:
            qs = Match.objects.filter(
                necessidade__cliente=user.cliente_profile,
                is_active=True
            )

        if status:
            qs = qs.filter(status=status)

        return qs.select_related(
            'necessidade',
            'necessidade__cliente',
            'necessidade__category',
            'empreendedor',
            'empreendedor__category',
        )



class MatchDetailView(LoginRequiredMixin, DetailView):
    """
    Detalhes de um match
    """
    model = Match
    template_name = 'marketplace/match_detail.html'
    context_object_name = 'match'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_empreendedor:
            return Match.objects.filter(empreendedor=user.empreendedor_profile)
        else:
            return Match.objects.filter(necessidade__cliente=user.cliente_profile)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message_form'] = MessageForm()
        context['messages'] = Message.objects.filter(
            match=self.object
        ).select_related('sender').order_by('date_created')
        return context


class MatchResponseView(LoginRequiredMixin, UpdateView):
    """
    Empreendedor responde a uma necessidade
    """
    model = Match
    form_class = MatchResponseForm
    template_name = 'marketplace/match_response.html'
    
    def get_queryset(self):
        return Match.objects.filter(
            empreendedor=self.request.user.empreendedor_profile,
            status='novo'
        )
    
    def form_valid(self, form):
        form.instance.status = 'em_conversa'
        messages.success(self.request, 'Resposta enviada com sucesso!')
        return super().form_valid(form)


class MatchUpdateView(LoginRequiredMixin, View):
    """
    Atualizar status de um match
    """
    def post(self, request, pk, *args, **kwargs):
        match = get_object_or_404(Match, pk=pk)
        status = request.POST.get('status')
        
        # Verifica permissão
        if request.user.is_empreendedor and match.empreendedor.user == request.user:
            pass  # Empreendedor pode atualizar
        elif not request.user.is_empreendedor and match.necessidade.cliente.user == request.user:
            pass  # Cliente pode atualizar
        else:
            messages.error(request, 'Você não tem permissão para atualizar este match.')
            return redirect('marketplace:dashboard')
        
        if status in ['visualizado', 'em_conversa', 'proposta_enviada', 'aceito', 'recusado', 'fechado']:
            match.status = status
            match.save()
            messages.success(request, f'Status atualizado para: {match.get_status_display()}')
        
        return redirect('marketplace:match-detail', pk=pk)


class MatchMessageView(LoginRequiredMixin, CreateView):
    """
    Enviar mensagem em um match
    """
    model = Message
    form_class = MessageForm
    
    def dispatch(self, request, *args, **kwargs):
        self.match = get_object_or_404(Match, pk=kwargs['pk'])
        
        # Verifica permissão
        if request.user.is_empreendedor:
            if self.match.empreendedor.user != request.user:
                return redirect('marketplace:dashboard')
        else:
            if self.match.necessidade.cliente.user != request.user:
                return redirect('marketplace:dashboard')
        
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.match = self.match
        form.instance.sender = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Mensagem enviada!')
        return response
    
    def get_success_url(self):
        return reverse('marketplace:match-detail', kwargs={'pk': self.match.pk})


class SearchView(ListView):
    """
    Busca geral na plataforma
    """
    template_name = 'marketplace/search.html'
    context_object_name = 'results'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if not query:
            return []
        
        # Busca em empreendedores
        empreendedores = Empreendedor.objects.filter(
            Q(business_name__icontains=query) |
            Q(description__icontains=query) |
            Q(services__icontains=query) |
            Q(location__icontains=query),
            is_active=True
        ).select_related('category')[:20]
        
        return empreendedores
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context