from django.contrib.auth.models import Group
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from community.constants import COMMUNITY_ADMIN
from community.utils import (create_groups, assign_permissions, remove_groups,
                             rename_groups)
from community.permissions import (groups_templates, group_permissions)


@receiver(post_save, sender='community.Community',
          dispatch_uid="manage_groups")
def manage_community_groups(sender, instance, created, **kwargs):
    """Manage user groups and user permissions for a particular Community"""
    name = instance.name
    if created:
        groups = create_groups(name, groups_templates)
        assign_permissions(
            instance, groups, groups_templates, group_permissions)
        community_admin_group = next(
            g for g in groups if g.name == COMMUNITY_ADMIN.format(name))
        instance.admin.join_group(community_admin_group)
        instance.add_member(instance.admin)
        instance.save()
    else:
        if name != instance.original_name and instance.original_name:
            rename_groups(instance.original_name, instance.name)
        if instance.admin != instance.original_admin and \
           instance.original_admin is not None:
            community_admin_group = \
                get_object_or_404(Group, name=COMMUNITY_ADMIN.format(name))
            instance.original_admin.leave_group(
                community_admin_group)
            instance.admin.join_group(community_admin_group)
            if instance.admin not in instance.members.all():
                instance.add_member(instance.admin)
                instance.save()


@receiver(post_delete, sender='community.Community',
          dispatch_uid="remove_groups")
def remove_community_groups(sender, instance, **kwargs):
    """Remove user groups for a particular Community instance"""
    remove_groups(instance.name)
