"""
Models principais do Marketplace Medusa
Define a estrutura de dados para usuários, empreendedores, clientes e matches
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone


class User(AbstractUser):
    """
    Model de usuário customizado que suporta múltiplos tipos de perfil
    """
    USER_TYPE_CHOICES = (
        ('cliente', 'Cliente'),
        ('empreendedor', 'Empreendedor'),
    )
    
    user_type = models.CharField(
        max_length=15, 
        choices=USER_TYPE_CHOICES, 
        default='cliente',
        help_text="Tipo de usuário na plataforma"
    )
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        verbose_name="Telefone",
        help_text="Número de telefone/WhatsApp"
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de criação"
    )
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_user_type_display()})"
    
    @property
    def is_empreendedor(self):
        """Verifica se o usuário é empreendedor"""
        return self.user_type == 'empreendedor'
    
    @property
    def is_cliente(self):
        """Verifica se o usuário é cliente"""
        return self.user_type == 'cliente'


class Category(models.Model):
    """
    Categorias de serviços/produtos oferecidos pelos empreendedores
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nome da categoria"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descrição"
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Ícone da categoria (ex: fa-hammer)"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Ativa"
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Ordem de exibição"
    )
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Empreendedor(models.Model):
    """
    Perfil do empreendedor com informações do negócio
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='empreendedor_profile',
        limit_choices_to={'user_type': 'empreendedor'}
    )
    business_name = models.CharField(
        max_length=200,
        verbose_name="Nome do negócio"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='empreendedores',
        verbose_name="Categoria principal"
    )
    description = models.TextField(
        verbose_name="Descrição do negócio",
        help_text="Descreva o que seu negócio faz e como pode ajudar clientes"
    )
    location = models.CharField(
        max_length=200,
        verbose_name="Localização",
        help_text="Bairro, cidade ou zona onde atua"
    )
    whatsapp = models.CharField(
        max_length=20,
        verbose_name="WhatsApp",
        help_text="Número para contato direto"
    )
    price_range = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Faixa de preço",
        help_text="Ex: A partir de 500 MT, Entre 1000-5000 MT, Sob consulta"
    )
    services = models.TextField(
        verbose_name="Serviços oferecidos",
        help_text="Liste os principais serviços ou produtos (um por linha)"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Perfil ativo"
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name="Verificado"
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de criação"
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Última atualização"
    )
    
    class Meta:
        verbose_name = "Empreendedor"
        verbose_name_plural = "Empreendedores"
        ordering = ['business_name']
    
    def __str__(self):
        return f"{self.business_name} - {self.user.get_full_name() or self.user.username}"
    
    def get_absolute_url(self):
        """URL para visualizar o perfil do empreendedor"""
        return reverse('empreendedor-detail', kwargs={'pk': self.pk})
    
    @property
    def services_list(self):
        """Retorna a lista de serviços como array"""
        return [s.strip() for s in self.services.split('\n') if s.strip()]


class Cliente(models.Model):
    """
    Perfil do cliente
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cliente_profile',
        limit_choices_to={'user_type': 'cliente'}
    )
    location = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Localização",
        help_text="Onde você está localizado"
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de criação"
    )
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} (Cliente)"


class Necessidade(models.Model):
    """
    Necessidade/problema publicado por um cliente
    """
    STATUS_CHOICES = (
        ('aberto', 'Aberto'),
        ('em_conversa', 'Em Conversa'),
        ('fechado', 'Fechado'),
        ('cancelado', 'Cancelado'),
    )
    
    URGENCY_CHOICES = (
        ('baixa', 'Baixa'),
        ('normal', 'Normal'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    )
    
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='necessidades',
        verbose_name="Cliente"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Ex: Preciso de um eletricista urgente"
    )
    description = models.TextField(
        verbose_name="Descrição",
        help_text="Descreva detalhadamente o que você precisa"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='necessidades',
        verbose_name="Categoria"
    )
    location = models.CharField(
        max_length=200,
        verbose_name="Localização",
        help_text="Onde o serviço deve ser realizado"
    )
    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Orçamento (MT)",
        help_text="Quanto você pretende gastar (opcional)"
    )
    urgency = models.CharField(
        max_length=10,
        choices=URGENCY_CHOICES,
        default='normal',
        verbose_name="Urgência"
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='aberto',
        verbose_name="Status"
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de criação"
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Última atualização"
    )
    
    class Meta:
        verbose_name = "Necessidade"
        verbose_name_plural = "Necessidades"
        ordering = ['-date_created']
    
    def __str__(self):
        return f"{self.title} - {self.cliente.user.get_full_name() or self.cliente.user.username}"
    
    def get_absolute_url(self):
        """URL para visualizar a necessidade"""
        return reverse('marketplace:necessidade-detail', kwargs={'pk': self.pk})


class Match(models.Model):
    """
    Conexão entre uma necessidade e um empreendedor
    """
    STATUS_CHOICES = (
        ('novo', 'Novo'),
        ('visualizado', 'Visualizado'),
        ('em_conversa', 'Em Conversa'),
        ('proposta_enviada', 'Proposta Enviada'),
        ('aceito', 'Aceito'),
        ('recusado', 'Recusado'),
        ('fechado', 'Fechado'),
    )
    
    necessidade = models.ForeignKey(
        Necessidade,
        on_delete=models.CASCADE,
        related_name='matches',
        verbose_name="Necessidade"
    )
    empreendedor = models.ForeignKey(
        Empreendedor,
        on_delete=models.CASCADE,
        related_name='matches',
        verbose_name="Empreendedor"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='novo',
        verbose_name="Status"
    )
    message = models.TextField(
        blank=True,
        verbose_name="Mensagem",
        help_text="Mensagem personalizada do empreendedor para o cliente"
    )
    price_quote = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Orçamento (MT)",
        help_text="Orçamento proposto pelo empreendedor"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de criação"
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Última atualização"
    )
    
    class Meta:
        verbose_name = "Match"
        verbose_name_plural = "Matches"
        unique_together = ['necessidade', 'empreendedor']
        ordering = ['-date_created']
    
    def __str__(self):
        return f"Match: {self.empreendedor.business_name} x {self.necessidade.title}"
    
    def get_absolute_url(self):
        """URL para visualizar o match"""
        return reverse('match-detail', kwargs={'pk': self.pk})


class Message(models.Model):
    """
    Mensagens trocadas entre clientes e empreendedores
    """
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name="Match"
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name="Remetente"
    )
    content = models.TextField(
        verbose_name="Conteúdo"
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name="Lida"
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de envio"
    )
    
    class Meta:
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"
        ordering = ['date_created']
    
    def __str__(self):
        return f"Mensagem de {self.sender} em {self.match}"