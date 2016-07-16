from django.contrib.auth.models import Group, Permission
from django.db import transaction
from guardian.shortcuts import assign_perm

from meetup.permissions import groups_templates, group_permissions


@transaction.atomic
def create_groups(meetup_location):
    """Create groups for a Meetup Location instance using its name

    :param meetup_location: string name of meetup location
    :return: list of meetup location Group objects
    """
    meetup_location_groups = []
    for key, group_name in groups_templates.items():
        group, created = Group.objects.get_or_create(
            name=group_name.format(meetup_location))
        meetup_location_groups.append(group)
    return meetup_location_groups


@transaction.atomic
def remove_groups(meetup_location):
    """Remove groups for a particular Meetup Location instance using its name

    :param meetup_location: string name of meetup location
    """
    name = "{0}:".format(meetup_location)
    Group.objects.filter(name__startswith=name).delete()


def get_groups(meetup_location):
    """Get groups of a particular Meetup Location instance using its name

    :param meetup_location: string name of Meetup Location
    :return: list of Group objects
    """
    name = "{0}:".format(meetup_location)
    return Group.objects.filter(name__startswith=name)


def assign_permissions(meetup_location, groups):
    """Assign row-level permissions to meetup location groups and meetup location object

    :param meetup_location: Meetup Location object
    :param groups: list of Group objects
    """
    for key, group_name in groups_templates.items():
        group = next(
            g for g in groups if g.name == group_name.format(meetup_location.name))
        for perm in group_permissions[key]:
            if (perm.endswith('meetup') or perm.endswith('meetuplocation') or
                    perm.endswith('rsvp') or perm.endswith('comment')):
                group.permissions.add(Permission.objects.get(codename=perm))
                group.save()
            else:
                assign_perm(perm, group, meetup_location)


'''
# no method of knowing if and when the name of meetup location is changed yet.

@transaction.atomic
def rename_groups(old_meetup_location, new_meetup_location):
    """Rename groups bound to a Meetup Location instance

    :param old_meetup_location: string old name of the meetup location
    :param new_meetup_location: string new name of the meetup location
    :return: list of meetup location new Group objects
    """
    name = "{0}:".format(old_meetup_location)
    groups = Group.objects.filter(name__startswith=name)
    new_meetup_location_groups = []
    for group in groups:
        old_name, group_name = group.name.rsplit(":", 1)
        group.name = "{0}:{1}".format(new_meetup_location, group_name)
        group.save()
        new_meetup_location_groups.append(group)
    return new_meetup_location_groups
'''
