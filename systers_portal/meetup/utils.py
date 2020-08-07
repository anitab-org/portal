from django.contrib.auth.models import Group, Permission
from django.core.mail import send_mail
from django.db import transaction
from django.template.loader import render_to_string

from meetup.permissions import groups_templates, group_permissions

from meetup.models import Rsvp

from users.models import UserSetting

from systers_portal.settings.dev import FROM_EMAIL


@transaction.atomic
def create_groups(meetup):
    """Create groups for a Meetup Location instance using its name

    :param meetup:
    :param meetup_location: string name of meetup location
    :return: list of meetup location Group objects
    """
    meetup_groups = []
    for key, group_name in groups_templates.items():
        group, created = Group.objects.get_or_create(
            name=group_name.format(meetup))
        meetup_groups.append(group)
    return meetup_groups


@transaction.atomic
def remove_groups(meetup):
    """Remove groups for a particular Meetup Location instance using its name
    """
    name = "{0}:".format(meetup)
    Group.objects.filter(name__startswith=name).delete()


def get_groups(meetup):
    """Get groups of a particular Meetup Location instance using its name

    :param meetup:
    :return: list of Group objects
    """
    name = "{0}:".format(meetup)
    return Group.objects.filter(name__startswith=name)


def assign_permissions(meetup, groups):
    """Assign row-level permissions to meetup location groups and meetup location object
    :param groups: list of Group objects
    """
    for key, group_name in groups_templates.items():
        group = next(
            g for g in groups if g.name == group_name.format(meetup.title))
        for perm in group_permissions[key]:
            group.permissions.add(Permission.objects.filter(codename=perm).first())
            group.save()


def send_reminder(meetup):
    rsvp_list = Rsvp.objects.filter(meetup=meetup)
    subject = "Reminder for {0}".format(meetup)
    for rsvp in rsvp_list:
        setting = UserSetting.objects.get(user=rsvp.user)
        if setting.reminder:
            html_text = render_to_string("templates/meetup/reminder.html",
                                         context={'meetup': meetup,
                                                  'user': rsvp.user})
            send_mail(
                subject,
                'Reminder Mail',
                FROM_EMAIL,
                [rsvp.user.user.email],
                html_message=html_text,
            )


def notify_location(meetup):
    rsvp_list = Rsvp.objects.filter(meetup=meetup)
    subject = "Notification for change in location for {0}".format(meetup)
    for rsvp in rsvp_list:
        setting = UserSetting.objects.get(user=rsvp.user)
        if setting.location_change:
            html_text = render_to_string("templates/meetup/location_change_email.html",
                                         context={'meetup': meetup,
                                                  'user': rsvp.user})
            send_mail(
                subject,
                'Change in Location',
                FROM_EMAIL,
                [rsvp.user.user.email],
                html_message=html_text,
            )


def notify_time(meetup):
    rsvp_list = Rsvp.objects.filter(meetup=meetup)
    subject = "Notification for change in location for {0}".format(meetup)
    for rsvp in rsvp_list:
        setting = UserSetting.objects.get(user=rsvp.user)
        if setting.time_change:
            html_text = render_to_string("templates/meetup/time_change_email.html",
                                         context={'meetup': meetup,
                                                  'user': rsvp.user})
            send_mail(
                subject,
                'Time Changed',
                FROM_EMAIL,
                [rsvp.user.user.email],
                html_message=html_text,
            )
