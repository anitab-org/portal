from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from meetup.constants import ADMIN
from meetup.utils import (create_groups, assign_permissions, remove_groups)


@receiver(post_save, sender='meetup.MeetupLocation',
          dispatch_uid="manage_groups")
def manage_meetup_location_groups(sender, instance, created, **kwargs):
    """Manage user groups and user permissions for a particular MeetupLocation"""
    name = instance.name
    if created:
        groups = create_groups(name)
        assign_permissions(instance, groups)
        meetup_location_admin_group = next(
            g for g in groups if g.name == ADMIN.format(name))
        instance.admin.join_group(meetup_location_admin_group)
        instance.add_member(instance.admin)
        instance.save()


@receiver(post_delete, sender='meetup.MeetupLocation',
          dispatch_uid="remove_groups")
def remove_meetup_location_groups(sender, instance, **kwargs):
    """Remove user groups for a particular Meetup Location"""
    remove_groups(instance.name)
