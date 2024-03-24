from django import template
register = template.Library()


@register.simple_tag(name='get_total_client')
def get_total_client(total_clients , machine):

    return total_clients[machine.id]
  
     



        

