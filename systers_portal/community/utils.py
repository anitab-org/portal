from django.contrib.auth.models import Group, Permission
from guardian.shortcuts import assign_perm

from community.permissions import groups_templates, group_permissions


def create_groups(community_name):
    """Create groups for a particular Community instance using its name

    :param community_name: string name of community
    :return: list of community Group objects
    """
    community_groups = []
    for key, group_name in groups_templates.items():
        group, created = Group.objects.get_or_create(
            name=group_name.format(community_name))
        community_groups.append(group)
    return community_groups


def remove_groups(community_name):
    """Remove groups for a particular Community instance using its name

    :param community_name: string name of community
    """
    name = "{0}:".format(community_name)
    Group.objects.filter(name__startswith=name).delete()


def assign_permissions(community, groups):
    """Assign row-level permissions to community groups and community object

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
