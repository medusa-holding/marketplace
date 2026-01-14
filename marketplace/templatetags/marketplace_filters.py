"""
Filtros customizados para templates do marketplace
"""

from django import template
from django.db.models import Q

register = template.Library()


@register.filter
def filter_status(matches, status):
    if not status:
        return matches

    try:
        return matches.filter(status=status)
    except Exception:
        # Evita quebrar caso venha lista ou queryset já fatiado
        return matches



@register.filter
def has_match(necessidade, empreendedor):
    """
    Verifica se um empreendedor já se candidatou a uma necessidade
    Uso: {% if necessidade|has_match:user.empreendedor_profile %}
    """
    from marketplace.models import Match
    return Match.objects.filter(
        necessidade=necessidade,
        empreendedor=empreendedor,
        is_active=True
    ).exists()


@register.filter
def get_match(necessidade, empreendedor):
    """
    Retorna o match entre uma necessidade e um empreendedor
    Uso: {% with match=necessidade|get_match:user.empreendedor_profile %}
    """
    from marketplace.models import Match
    try:
        return Match.objects.get(
            necessidade=necessidade,
            empreendedor=empreendedor,
            is_active=True
        )
    except Match.DoesNotExist:
        return None