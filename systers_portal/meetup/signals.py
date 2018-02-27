from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

from meetup.models import MeetupLocation
from meetup.constants import COMMUNITY_MEMBER, COMMUNITY_MODERATOR, COMMUNITY_LEADER
from meetup.utils import (create_groups, assign_permissions, remove_groups)
from users.models import SystersUser


@receiver(post_save, sender=MeetupLocation, dispatch_uid="manage_groups")
def manage_meetup_location_groups(sender, instance, created, **kwargs):
    """Manage user groups and user permissions for a particular MeetupLocation"""
    name = instance.name
    if created:
        groups = create_groups(name)
        assign_permissions(instance, groups)
        community_leader_group = next(
            g for g in groups if g.name == COMMUNITY_LEADER.format(name))
        instance.leader.join_group(community_leader_group)
        instance.save()


@receiver(post_delete, sender=MeetupLocation, dispatch_uid="remove_groups")
def remove_meetup_location_groups(sender, instance, **kwargs):
    """Remove user groups for a particular Meetup Location"""
    remove_groups(instance.name)


@receiver(m2m_changed, sender=MeetupLocation.members.through,
          dispatch_uid="add_members")
def add_meetup_location_members(sender, **kwargs):
    """Add permissions to a user when she is added as a Meetup Location member"""
    instance = kwargs.pop('instance', None)
    action = kwargs.pop('action', None)
    pk_set = kwargs.pop('pk_set', None)
    if action == "pre_add":
        systersuser = SystersUser.objects.get(pk=list(pk_set)[0])
        members_group = get_object_or_404(Group, name=COMMUNITY_MEMBER.format(instance.name))
        if not systersuser.is_group_member(members_group.name):
            systersuser.join_group(members_group)


@receiver(m2m_changed, sender=MeetupLocation.moderators.through,
          dispatch_uid="add_moderators")
def add_meetup_location_moderators(sender, **kwargs):
    """Add permissions to a user when she is added as a Meetup Location moderator"""
    instance = kwargs.pop('instance', None)
    action = kwargs.pop('action', None)
    pk_set = kwargs.pop('pk_set', None)
    if action == "pre_add":
        systersuser = SystersUser.objects.get(pk=list(pk_set)[0])
        moderators_group = get_object_or_404(Group, name=COMMUNITY_MODERATOR.format(instance.name))
        if not systersuser.is_group_member(moderators_group.name):
            systersuser.join_group(moderators_group)


@receiver(m2m_changed, sender=MeetupLocation.members.through,
          dispatch_uid="delete_members")
def delete_meetup_location_members(sender, **kwargs):
    """Delete permissions from a user when she is removed as a Meetup Location member"""
    instance = kwargs.pop('instance', None)
    action = kwargs.pop('action', None)
    pk_set = kwargs.pop('pk_set', None)
    if action == "pre_remove":
        systersuser = SystersUser.objects.get(pk=list(pk_set)[0])
        members_group = get_object_or_404(Group, name=COMMUNITY_MEMBER.format(instance.name))
        if systersuser.is_group_member(members_group.name):
            systersuser.leave_group(members_group)


@receiver(m2m_changed, sender=MeetupLocation.moderators.through,
          dispatch_uid="delete_moderators")
def delete_meetup_location_moderators(sender, **kwargs):
    """Delete permissions from a user when she is removed as a Meetup Location moderator"""
    instance = kwargs.pop('instance', None)
    action = kwargs.pop('action', None)
    pk_set = kwargs.pop('pk_set', None)
    if action == "pre_remove":
        systersuser = SystersUser.objects.get(pk=list(pk_set)[0])
        moderators_group = get_object_or_404(Group, name=COMMUNITY_MODERATOR.format(instance.name))
        if systersuser.is_group_member(moderators_group.name):
            systersuser.leave_group(moderators_group)
