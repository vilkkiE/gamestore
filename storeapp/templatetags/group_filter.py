from django import template
from django.contrib.auth.models import Group

register = template.Library()


# Checks if the given user belongs to the given group
@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    if group in user.groups.all():
        return True
    else:
        return False