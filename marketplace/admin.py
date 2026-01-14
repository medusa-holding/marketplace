"""
Configuração do Django Admin para o marketplace
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Category, Empreendedor, Cliente, 
    Necessidade, Match, Message
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin para usuários customizados"""
    list_display = ['username', 'email', 'get_full_name', 'user_type', 'phone', 'is_active']
    list_filter = ['user_type', 'is_active', 'is_staff', 'date_created']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('user_type', 'phone')
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin para categorias"""
    list_display = ['name', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name']
    ordering = ['order', 'name']


@admin.register(Empreendedor)
class EmpreendedorAdmin(admin.ModelAdmin):
    """Admin para empreendedores"""
    list_display = [
        'business_name', 'user', 'category', 
        'location', 'is_active', 'is_verified', 'date_created'
    ]
    list_filter = ['category', 'is_active', 'is_verified', 'date_created']
    search_fields = ['business_name', 'user__username', 'user__first_name', 'location']
    readonly_fields = ['date_created', 'date_updated']
    
    fieldsets = (
        ('Informações do Usuário', {
            'fields': ('user',)
        }),
        ('Informações do Negócio', {
            'fields': (
                'business_name', 'category', 'description', 
                'services', 'price_range'
            )
        }),
        ('Contato e Localização', {
            'fields': ('location', 'whatsapp')
        }),
        ('Status', {
            'fields': ('is_active', 'is_verified')
        }),
        ('Datas', {
            'fields': ('date_created', 'date_updated'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """Admin para clientes"""
    list_display = ['user', 'location', 'date_created']
    search_fields = ['user__username', 'user__first_name', 'location']
    readonly_fields = ['date_created']


@admin.register(Necessidade)
class NecessidadeAdmin(admin.ModelAdmin):
    """Admin para necessidades"""
    list_display = [
        'title', 'cliente', 'category', 
        'urgency', 'status', 'budget', 'date_created'
    ]
    list_filter = ['status', 'urgency', 'category', 'date_created']
    search_fields = ['title', 'description', 'cliente__user__username']
    readonly_fields = ['date_created', 'date_updated']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('title', 'description', 'cliente', 'category')
        }),
        ('Localização e Orçamento', {
            'fields': ('location', 'budget')
        }),
        ('Status', {
            'fields': ('urgency', 'status')
        }),
        ('Datas', {
            'fields': ('date_created', 'date_updated'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    """Admin para matches"""
    list_display = [
        'necessidade', 'empreendedor', 
        'status', 'price_quote', 'date_created'
    ]
    list_filter = ['status', 'is_active', 'date_created']
    search_fields = [
        'necessidade__title', 
        'empreendedor__business_name',
        'empreendedor__user__username'
    ]
    readonly_fields = ['date_created', 'date_updated']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin para mensagens"""
    list_display = ['match', 'sender', 'content_preview', 'is_read', 'date_created']
    list_filter = ['is_read', 'date_created']
    search_fields = ['content', 'sender__username']
    readonly_fields = ['date_created']
    
    def content_preview(self, obj):
        """Preview do conteúdo da mensagem"""
        if len(obj.content) > 50:
            return obj.content[:50] + '...'
        return obj.content
    content_preview.short_description = 'Conteúdo'