from django.db import models
from cities_light.models import City
from ckeditor.fields import RichTextField

from users.models import SystersUser


class Meetup(models.Model):
    """Manage details of Meetups of MeetupLocations"""
    title = models.CharField(max_length=50, verbose_name="Title", )
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Slug")
    date = models.DateField(verbose_name="Date")
    end_date = models.DateField(verbose_name="End Date", null=True)
    time = models.TimeField(verbose_name="Time", blank=True)
    end_time = models.TimeField(verbose_name="End Time", null=True)
    venue = models.CharField(max_length=512, verbose_name="Venue", blank=True)
    description = models.TextField(verbose_name="Description")
    leader = models.ForeignKey(SystersUser, null=True, blank=True, related_name='community_leader',
                               verbose_name="Community leader", on_delete=models.CASCADE)
    meetup_location = models.ForeignKey(
        City, verbose_name="Meetup Location", on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        SystersUser, null=True, verbose_name="Created By", on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Last Update")
    meetup_picture = models.ImageField(upload_to='meetup/pictures/',
                                       blank=True,
                                       null=True,
                                       verbose_name="Meetup picture")

    class Meta:
        permissions = (
            ("view_meetup_request", "View Meetup Request"),
            ('approve_meetup_request', 'Approve Meetup Request'),
            ('reject_meetup_request', 'Reject Meetup Request'),
            ('add_meetups', 'Add Meetups'),
            ('delete_meetups', 'Delete Meetup'),
            ('change_meetups', 'Change Meetup'),
            ('add_meetup_rsvp', 'Add Meetup RSVP'),
            ('add_support_request', 'Add Support Request'),
            ('edit_support_request', 'Edit Support Request'),
            ('delete_support_request', 'Delete Support Request'),
            ('approve_support_request', 'Approve Support Request'),
            ('reject_support_request', "Reject Support Request"),
            ('add_support_request_comment', 'Add Support Request Comment')
        )

    def __str__(self):
        return self.title


class RequestMeetup(models.Model):
    """Manage details of Meetup Requests of MeetupLocations"""
    title = models.CharField(max_length=50, verbose_name="Title", )
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Slug")
    date = models.DateField(verbose_name="Date")
    time = models.TimeField(verbose_name="Time", blank=True)
    venue = models.CharField(max_length=512, verbose_name="Venue", blank=True)
    description = RichTextField(verbose_name="Description")
    meetup_location = models.ForeignKey(
        City, verbose_name="Meetup Location", on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        SystersUser, null=True, verbose_name="Created By", on_delete=models.CASCADE)
    approved_by = models.ForeignKey(SystersUser, blank=True, null=True,
                                    related_name='approvedBy', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def get_verbose_fields(self):
        """Get verbose names of RequestMeetup object's model fields
        :return: list of tuples (verbosefieldname, fieldvalue)
        """
        return [(field.verbose_name, getattr(self, field.name)) for field in
                RequestMeetup._meta.fields]

    def __str__(self):
        return self.title


class Rsvp(models.Model):
    """ Users RSVP for particular meetup """
    user = models.ForeignKey(SystersUser, verbose_name="User", on_delete=models.CASCADE)
    meetup = models.ForeignKey(Meetup, verbose_name="Meetup", on_delete=models.CASCADE)
    coming = models.BooleanField(default=True)
    plus_one = models.BooleanField(default=False)

    class Meta:
        unique_together = (('user', 'meetup'),)

    def __str__(self):
        return "{0} RSVP for meetup {1}".format(self.user, self.meetup)


class SupportRequest(models.Model):
    """Manage details of various volunteering activities"""
    volunteer = models.ForeignKey(SystersUser, verbose_name="Volunteer", on_delete=models.CASCADE)
    meetup = models.ForeignKey(Meetup, verbose_name="Meetup", on_delete=models.CASCADE)
    description = models.TextField(verbose_name="Description", blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return "{0} volunteered for meetup {1}".format(self.volunteer, self.meetup)
