from datetime import datetime, timedelta

from django.db.models.signals import post_save, post_delete, post_migrate, pre_save
from django.dispatch import receiver
from pinax.notifications.models import NoticeType

from meetup.models import Meetup
from meetup.constants import COMMUNITY_LEADER
from meetup.utils import (create_groups, assign_permissions, remove_groups)

from users.scheduler import scheduler
from meetup.utils import notify_location, notify_time


@receiver(post_save, sender=Meetup, dispatch_uid="manage_groups")
def manage_meetup_groups(sender, instance, created, **kwargs):
    """Manage user groups and user permissions for a particular MeetupLocation"""
    name = instance.title
    if created:
        groups = create_groups(name)
        assign_permissions(instance, groups)
        community_leader_group = next(
            g for g in groups if g.name == COMMUNITY_LEADER.format(name))
        instance.leader.join_group(community_leader_group)
        instance.save()


@receiver(post_delete, sender=Meetup, dispatch_uid="remove_groups")
def remove_meetup_groups(sender, instance, **kwargs):
    """Remove user groups for a particular Meetup Location"""
    remove_groups(instance.title)


@receiver(post_migrate, dispatch_uid="create_notice_types")
def create_notice_types(sender, **kwargs):
    """Create notice types to send email notifications"""
    NoticeType.create("new_meetup", ("New Meetup"),
                      ("a new meetup has been added"))
    NoticeType.create("new_support_request", ("New Support Request"),
                      ("a user has added a support request"))
    NoticeType.create("support_request_approved", ("Support Request Approved"),
                      ("your support request has been approved"))
    NoticeType.create("new_meetup_request", ("New Meetup Request"),
                      ("a user has added a meetup request"))


@receiver(pre_save, sender=Meetup, dispatch_uid="location_change")
def notify_change(sender, instance, **kwargs):
    obj = Meetup.objects.filter(pk=instance.pk)
    if obj:
        if obj[0].date != instance.date or obj[0].time != instance.time:
            name = "Time for {0} Change Notify".format(instance.title)
            scheduler.add_job(notify_time, "date",
                              run_date=datetime.now() + timedelta(minutes=5),
                              args=[instance],
                              id=name, replace_existing=True)
        if obj[0].meetup_location != instance.meetup_location:
            name = "Location for {0} Change Notify".format(instance.title)
            scheduler.add_job(notify_location, "date",
                              run_date=datetime.now() + timedelta(minutes=5),
                              args=[instance],
                              id=name, replace_existing=True)
