import datetime
import logging
from datetime import timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django_apscheduler.jobstores import register_events, register_job

from django.conf import settings

from meetup.utils import send_reminder
from meetup.models import Meetup

from community.models import Community

from systers_portal.settings.dev import FROM_EMAIL

scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)


@register_job(scheduler, 'cron', day_of_week='mon', hour=5, minute=30, replace_existing=True)
def weekly_digest():
    communities = Community.objects.all()
    for community in communities:
        subject = "Weekly update from {0}".format(community)
        count = community.members.count()
        for member in community.members:
            html_text = \
                render_to_string("templates/community/weekly_digest_email.html",
                                 {'user': member,
                                  'count': count,
                                  'community': community})
            send_mail(
                subject,
                'Weekly Digest',
                FROM_EMAIL,
                [member.user.email],
                html_message=html_text,
            )


def start():
    if settings.DEBUG:
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    register_events(scheduler)
    scheduler.start()
    meetup_list = Meetup.objects.filter(date__gte=datetime.date.today())
    for meetup in meetup_list:
        name = "Reminder for {0}".format(meetup.title)
        scheduler.add_job(send_reminder, "date", run_date=meetup.date - timedelta(hours=1),
                          args=[meetup], id=name, replace_existing=True)
