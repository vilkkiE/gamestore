from django.contrib.auth.models import Group

new_group, created = Group.objects.get_or_create(name='developers')
new_group, created = Group.objects.get_or_create(name='players')