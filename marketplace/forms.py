"""
Forms do marketplace
Define os formulários para registro, perfis e interações
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import (
    User, Empreendedor, Cliente, Necessidade, 
    Match, Message, Category
)

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """
    Form de registro de usuário com seleção de tipo
    """
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        initial='cliente',
        label="Você é:"
    )
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label="Nome"
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label="Sobrenome"
    )
    email = forms.EmailField(
        required=True,
        label="E-mail"
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        label="Telefone/WhatsApp"
    )
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 
            'email', 'phone', 'user_type', 'password1', 'password2'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona classes CSS aos campos
        for field_name, field in self.fields.items():
            if field_name != 'user_type':
                field.widget.attrs['class'] = 'form-control'


class EmpreendedorProfileForm(forms.ModelForm):
    """
    Form para completar o perfil do empreendedor
    """
    class Meta:
        model = Empreendedor
        fields = [
            'business_name', 'category', 'description',
            'services', 'location', 'whatsapp', 'price_range'
        ]
        widgets = {
            'business_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Electricidade Moderna'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva o que seu negócio faz...'
            }),
            'services': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Liste seus serviços (um por linha)\nEx:\n- Instalação elétrica\n- Reparos\n- Manutenção'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Bairro Central, Maputo'
            }),
            'whatsapp': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '84 123 4567'
            }),
            'price_range': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: A partir de 500 MT, Sob consulta'
            }),
        }
        labels = {
            'business_name': 'Nome do seu negócio',
            'category': 'Categoria principal',
            'description': 'Descreva seu negócio',
            'services': 'Serviços que oferece',
            'location': 'Onde você atua',
            'whatsapp': 'WhatsApp para contato',
            'price_range': 'Preços (opcional)'
        }


class ClienteProfileForm(forms.ModelForm):
    """
    Form para completar o perfil do cliente
    """
    class Meta:
        model = Cliente
        fields = ['location']
        widgets = {
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Bairro Central, Maputo'
            }),
        }
        labels = {
            'location': 'Onde você está localizado'
        }


class NecessidadeForm(forms.ModelForm):
    """
    Form para criar/editar uma necessidade
    """
    class Meta:
        model = Necessidade
        fields = [
            'title', 'description', 'category', 
            'location', 'budget', 'urgency'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Preciso de um eletricista urgente'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Descreva detalhadamente o que você precisa...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Onde precisa do serviço'
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quanto pretende gastar (opcional)'
            }),
            'urgency': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'title': 'Título',
            'description': 'Descrição',
            'category': 'Categoria',
            'location': 'Localização',
            'budget': 'Orçamento (MT)',
            'urgency': 'Urgência'
        }


class MatchResponseForm(forms.ModelForm):
    """
    Form para empreendedor responder a uma necessidade
    """
    class Meta:
        model = Match
        fields = ['message', 'price_quote']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escreva uma mensagem para o cliente explicando como você pode ajudar...'
            }),
            'price_quote': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Orçamento proposto (MT) - opcional'
            }),
        }
        labels = {
            'message': 'Sua mensagem',
            'price_quote': 'Orçamento proposto'
        }


class MessageForm(forms.ModelForm):
    """
    Form para enviar mensagens
    """
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Digite sua mensagem...'
            }),
        }
        labels = {
            'content': 'Mensagem'
        }


class SearchForm(forms.Form):
    """
    Form para buscar empreendedores ou necessidades
    """
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar...'
        }),
        label=''
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True),
        required=False,
        empty_label="Todas as categorias",
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label=''
    )


class ContactForm(forms.Form):
    """
    Form de contato simples
    """
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu nome'
        }),
        label='Nome'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu e-mail'
        }),
        label='E-mail'
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Assunto'
        }),
        label='Assunto'
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Sua mensagem'
        }),
        label='Mensagem'
    )