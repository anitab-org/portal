from django.contrib.auth.models import Group, Permission
from django.db import transaction

from meetup.permissions import groups_templates, group_permissions


@transaction.atomic
def create_groups(meetup):
    """Create groups for a Meetup Location instance using its name

    :param meetup:
    :param meetup_location: string name of meetup location
    :return: list of meetup location Group objects
    """
    meetup_groups = []
    for key, group_name in groups_templates.items():
        group, created = Group.objects.get_or_create(
            name=group_name.format(meetup))
        meetup_groups.append(group)
    return meetup_groups


@transaction.atomic
def remove_groups(meetup):
    """Remove groups for a particular Meetup Location instance using its name
    """
    name = "{0}:".format(meetup)
    Group.objects.filter(name__startswith=name).delete()


def get_groups(meetup):
    """Get groups of a particular Meetup Location instance using its name

    :param meetup:
    :return: list of Group objects
    """
    name = "{0}:".format(meetup)
    return Group.objects.filter(name__startswith=name)


def assign_permissions(meetup, groups):
    """Assign row-level permissions to meetup location groups and meetup location object
    :param groups: list of Group objects
    """
    for key, group_name in groups_templates.items():
        group = next(
            g for g in groups if g.name == group_name.format(meetup.title))
        for perm in group_permissions[key]:
            group.permissions.add(Permission.objects.filter(codename=perm).first())
            group.save()
