from django import template

from machinery1.models import Client

register = template.Library()


@register.simple_tag(name='is_machine_already_applied')
def is_machine_already_applied(machine, user):
    applied = Client.objects.filter(machine=machine, user=user)
    if applied:
        return True
    else:
        return False
