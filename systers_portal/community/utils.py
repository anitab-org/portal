from django.contrib.auth.models import Group, Permission
from django.db import transaction
from guardian.shortcuts import assign_perm


@transaction.atomic
def create_groups(community_name, groups_templates):
    """Create groups for a particular Community instance using its name

    :param community_name: string name of community object
    :return: list of community Group objects
    """
    community_groups = []
    for key, group_name in groups_templates.items():
        group, created = Group.objects.get_or_create(
            name=group_name.format(community_name))
        community_groups.append(group)
    return community_groups


@transaction.atomic
def remove_groups(community_name):
    """Remove groups for a particular Community instance using its name

    :param community_name: string name of community object
    """
    name = "{0}:".format(community_name)
    Group.objects.filter(name__startswith=name).delete()


def get_groups(community_name):
    """Get groups of a particular Community instance using its name

    :param community_name: string name of Community
    :return: list of Group objects
    """
    name = "{0}:".format(community_name)
    return Group.objects.filter(name__startswith=name)


@transaction.atomic
def rename_groups(old_community_name, new_community_name):
    """Rename groups bound to a Community instance

    :param old_community_name: string old name of the community
    :param new_community_name: string new name of the community
    :return: list of community new Group objects
    """
    name = "{0}:".format(old_community_name)
    groups = Group.objects.filter(name__startswith=name)
    new_community_groups = []
    for group in groups:
        old_name, group_name = group.name.rsplit(":", 1)
        group.name = "{0}:{1}".format(new_community_name, group_name)
        group.save()
        new_community_groups.append(group)
    return new_community_groups


def assign_permissions(community, groups, groups_templates, group_permissions):
    """Assign row-level permissions to community groups and
       community object

    :param community: Community object
    :param groups: list of Group objects
    """
    for key, group_name in groups_templates.items():
        group = next(
            g for g in groups if g.name == group_name.format(community.name))
        for perm in group_permissions[key]:
            if perm.endswith('tag') or perm.endswith('resourcetype'):
                group.permissions.add(Permission.objects.get(codename=perm))
                group.save()
            else:
                assign_perm(perm, group, community)
