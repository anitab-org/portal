from django.contrib.auth.models import Group, Permission, User
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from allauth.account.signals import user_signed_up
from guardian.shortcuts import assign_perm

from dashboard.models import Community, SysterUser


generic_groups = {"content_contributor": "Content Contributor for {0}",
                  "content_manager": "Content Manager for {0}",
                  "user_content_manager": "User and Content Manager for {0}",
                  "community_admin": "Community Admin for {0}"}

content_contributor_permissions = [
    "add_community_resource",
    "change_community_resource",
    "change_community_page",
    "add_community_news",
    "change_community_news",
]

content_manager_permissions = content_contributor_permissions + [
    "delete_community_resource",
    "add_community_page",
    "delete_community_page",
    "delete_community_news",
    "delete_tag",
    "delete_resourcetype",
]

user_content_manager_permissions = content_manager_permissions + [
    "add_community_systeruser",
    "change_community_systeruser",
    "delete_community_systeruser",
]

community_admin_permissions = user_content_manager_permissions + [
    "change_community",
]

dashboard_group_permissions = {
    "content_contributor": content_contributor_permissions,
    "content_manager": content_manager_permissions,
    "user_content_manager": user_content_manager_permissions,
    "community_admin": community_admin_permissions
}


@receiver(post_save, sender=Community, dispatch_uid="create_groups")
def create_community_groups(sender, instance, created, **kwargs):
    """Create user groups for a particular Community instance and assign
    permissions to each group"""
    if created:
        create_groups(instance.name)
        assign_permissions(instance)
        join_group(instance.community_admin,
                   generic_groups["community_admin"].format(instance.name))
    else:
        if instance.name != instance.original_name:
            delede_groups(instance.original_name)
            create_groups(instance.name)
            assign_permissions(instance)
        if instance.community_admin != instance.original_community_admin:
            community_admin_group_name = generic_groups[
                "community_admin"].format(instance.name)
            leave_group(instance.original_community_admin,
                        community_admin_group_name)
            join_group(instance.community_admin, community_admin_group_name)
    grant_access_to_parent_community(instance)


@receiver(post_delete, sender=Community, dispatch_uid="remove_groups")
def remove_community_groups(sender, instance, **kwargs):
    """Remove user groups for this particular Community instance"""
    delede_groups(instance.name)


@receiver(user_signed_up)
def create_syster_user(sender, **kwargs):
    """Keep User and SysterUser synchronized. Create a SystersUser instance on
    receiving a signal about new user signup.
    """
    user = kwargs.get('user')
    if user is not None:
        syster_user = SysterUser(user=user)
        syster_user.save()


@receiver(m2m_changed, sender=User.groups.through,
          dispatch_uid="give_basic_access")
def give_basic_access(sender, instance, action, **kwargs):
    """Give basic access to users who are members of at least one community group.

    If you decide to give user direct permissions instead of groups, then you
    should manually make user staff member and add him to the "Generic
    permissions" group, if you want the user to have those generic permissions.
    """
    if isinstance(instance, User):
        if action == "post_add" or action == "post_remove":
            has_generic_access = instance.groups.filter(
                name="Generic permissions").exists()
            is_member_other_groups = instance.groups.exclude(
                name="Generic permissions").exists()
            if is_member_other_groups:
                if has_generic_access:
                    if not instance.is_staff:
                        instance.is_staff = True
                else:
                    m2m_changed.disconnect(give_basic_access,
                                           sender=User.groups.through,
                                           dispatch_uid="give_basic_access")
                    instance.groups.add(
                        Group.objects.get(name="Generic permissions"))
                    instance.is_staff = True
            else:
                m2m_changed.disconnect(give_basic_access,
                                       sender=User.groups.through,
                                       dispatch_uid="give_basic_access")
                instance.groups.remove(
                    Group.objects.get(name="Generic permissions"))
                instance.is_staff = False
            instance.save()
            m2m_changed.connect(give_basic_access, sender=User.groups.through,
                                dispatch_uid="give_basic_access")


def create_groups(community_name):
    """Create groups for a particular Community instance using its name

    :param community_name: string name of community
    """
    for key, group_name in generic_groups.items():
        Group.objects.get_or_create(name=group_name.format(community_name))


def delede_groups(community_name):
    """Delete groups that were created using community name

    :param community_name: string name of community
    """
    for key, group_name in generic_groups.items():
        Group.objects.get(name=group_name.format(community_name)).delete()


def assign_permissions(community):
    """Assign specific permissions for each group

    :param community: Community object
    """
    for key, group_name in generic_groups.items():
        group = Group.objects.get(name=group_name.format(community.name))
        for perm in dashboard_group_permissions[key]:
            if perm.endswith('tag') or perm.endswith('resourcetype'):
                group.permissions.add(Permission.objects.get(codename=perm))
                group.save()
            else:
                assign_perm(perm, group, community)


def grant_access_to_parent_community(community):
    """Make members of parent community "Community Admin" group, also members
    of subcommunity's "Community Admin" group.

    :param community: Community object
    """
    if community.parent_community is not None:
        community_admin_group = Group.objects.get(
            name=generic_groups["community_admin"].format(
                community.name))
        parent_community_admin_users = User.objects.filter(
            groups__name=generic_groups["community_admin"].format(
                community.parent_community.name))
        for user in parent_community_admin_users:
            community_admin_group.user_set.add(user)


def join_group(user, group_name):
    """Make user member of a group

    :param user: SysterUser object
    :param group_name: string full name of a group
    """
    group = get_object_or_404(Group, name=group_name)
    user.user.groups.add(group)


def leave_group(user, group_name):
    """Remove the user from group members

    :param user:
    :param group_name:
    :return:
    """
    group = get_object_or_404(Group, name=group_name)
    user.user.groups.remove(group)
