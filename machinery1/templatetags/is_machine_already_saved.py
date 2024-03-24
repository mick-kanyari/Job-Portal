from django import template

from machinery1.models import BookmarkMachine

register = template.Library()


@register.simple_tag(name='is_machine_already_saved')
def is_machine_already_saved(machine, user):
    applied = BookmarkMachine.objects.filter(machine=machine, user=user)
    if applied:
        return True
    else:
        return False
