from django.contrib.auth.models import Group

from community.permissions import groups_templates


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
