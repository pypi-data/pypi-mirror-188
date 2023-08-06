# importing group class from django
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# import User model
from  django.contrib.auth.models import User 
def add_group(group_name, permitt):

    # group_name = input('What is the preferred group name? ')

    new_group, created = Group.objects.get_or_create(name = group_name)

    # Code to add permission to group
    ct = ContentType.objects.get_for_model(User)

    # If I want to add 'Can go Haridwar' permission to level0 ?
    # permitt = input('What permission should they have? ')
    permit_codename = permitt.replace(" ", "_")

    permission = Permission.objects.create(codename =permit_codename,
    										name = permitt,
    												content_type = ct)
    new_group.permissions.add(permission)

   




