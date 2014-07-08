from django.db.models.signals import post_syncdb
from django.contrib.auth.models import Group, Permission
from dashboard import models


content_contributor_permissions = [
    "add_resource",
    "change_resource",
    "change_communitypage",
    "add_news",
    "change_news",
    "add_tag",
    "change_tag",
    "add_resourcetype",
    "change_resourcetype",
]

content_manager_permissions = content_contributor_permissions + [
    "delete_resource",
    "add_communitypage",
    "delete_communitypage",
    "delete_news",
    "delete_tag",
    "delete_resourcetype",
]

user_content_manager_permissions = content_manager_permissions + [
    "add_systeruser",
    "change_systeruser",
    "delete_systeruser",
]

community_admin_permissions = user_content_manager_permissions + [
    "change_community",
]

dashboard_group_permissions = {
    "Content Contributor": content_contributor_permissions,
    "Content Manager": content_manager_permissions,
    "User and Content Manager": user_content_manager_permissions,
    "Community Admin": community_admin_permissions
}


def create_user_groups(sender, **kwargs):
    """Create user groups and assign permissions to each group

    :param sender: models module that was just installed
    """
    verbosity = kwargs.get("verbosity")
    if verbosity > 0:
        print "Initializing data post_syncdb"
    for group in dashboard_group_permissions:
        role, created = Group.objects.get_or_create(name=group)
        if verbosity > 1 and created:
            print "Creating group {0}".format(group)
        for perm in dashboard_group_permissions[group]:
            role.permissions.add(Permission.objects.get(codename=perm))
            if verbosity > 1:
                print "Permitting {0} to {1}".format(group, perm)
        role.save()

post_syncdb.connect(create_user_groups, sender=models)
