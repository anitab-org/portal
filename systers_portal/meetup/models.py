from django.db import models
from cities_light.models import City
from ckeditor.fields import RichTextField


from users.models import SystersUser


class MeetupLocation(models.Model):
    """Manage details of Meetup Location groups"""
    name = models.CharField(max_length=255, unique=True, verbose_name="Name")
    slug = models.SlugField(max_length=150, unique=True, verbose_name="Slug")
    location = models.ForeignKey(City, verbose_name="Location")
    description = RichTextField(verbose_name="Description")
    email = models.EmailField(max_length=255, blank=True, verbose_name="Email")
    leader = models.ForeignKey(SystersUser, null=True, blank=True, related_name='community_leader',
                               verbose_name="Community leader")
    moderators = models.ManyToManyField(SystersUser,
                                        related_name="community_moderators",
                                        verbose_name="Community Moderators")
    members = models.ManyToManyField(SystersUser, blank=True,
                                     related_name="community_members",
                                     verbose_name="Community Members")
    sponsors = RichTextField(verbose_name="Sponsors", blank=True)
    join_requests = models.ManyToManyField(SystersUser,
                                           related_name="Join_Requests",
                                           verbose_name="Join Requests",
                                           blank=True)

    class Meta:
        permissions = (
            ('add_meetup_location_member', 'Add meetup location member'),
            ('delete_meetup_location_member', 'Delete meetup location member'),
            ('add_meetup_location_moderator', 'Add meetup location moderator'),
            ('delete_meetup_location_moderator', 'Delete meetup location moderator'),
            ('approve_meetup_location_joinrequest', 'Approve meetup location join request'),
            ('reject_meetup_location_joinrequest', 'Reject meetup location join request'),
            ('approve_meetup_location_meetuprequest', 'Approve meetup location meetup request'),
            ('reject_meetup_location_meetuprequest', 'Reject meetup location meetup request'),
            ('view_meetup_location_meetuprequest', 'View meetup location meetup request'),
            ('approve_meetup_comment', 'Approve comment for a meetup'),
            ('reject_meetup_comment', 'Reject comment for a meetup'),
            ('add_meetup_rsvp', 'RSVP for a meetup'),
            ('approve_support_request', 'Approve support request'),
            ('reject_support_request', 'Reject support request'),
            ('add_support_request_comment', 'Add comment for a support request'),
            ('edit_support_request_comment', 'Edit comment for a support request'),
            ('delete_support_request_comment', 'Delete comment for a support request'),
            ('approve_support_request_comment', 'Approve comment for a support request'),
            ('reject_support_request_comment', 'Reject comment for a support request')
        )

    def __str__(self):
        return self.name


class RequestMeetupLocation(models.Model):
    """Manage details of Meetup Location requests"""
    name = models.CharField(max_length=255, unique=True, verbose_name="Name of the Meetup Location."
                            "(Naming convention for Systers meetup location is City+Systers."
                            "e.g.London Systers, Boston Systers.)")
    slug = models.SlugField(max_length=150, unique=True,
                            verbose_name="Slug of the Meetup Location")
    location = models.ForeignKey(City, verbose_name="Location")
    description = RichTextField(
        verbose_name="Description of the Meetup Location")
    email = models.EmailField(max_length=255, blank=True,
                              verbose_name="Email of the Meetup Location if any.")
    user = models.ForeignKey(
        SystersUser, related_name='createdby', verbose_name="Requested By")
    approved_by = models.ForeignKey(SystersUser, blank=True, null=True,
                                    related_name='approvedby', verbose_name="Approved By")
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name="Date Created")
    is_approved = models.BooleanField(
        default=False, verbose_name="Is this Approved?")

    def get_verbose_fields(self):
        """Get verbose names of RequestMeetupLocation object's model fields
        :return: list of tuples (verbosefieldname, fieldvalue)
        """

        return [(field.verbose_name, getattr(self, field.name)) for field in
                RequestMeetupLocation._meta.fields]

    def __str__(self):
        return self.name


class Meetup(models.Model):
    """Manage details of Meetups of MeetupLocations"""
    title = models.CharField(max_length=50, verbose_name="Title",)
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Slug")
    date = models.DateField(verbose_name="Date")
    end_date = models.DateField(verbose_name="End Date", null=True)
    time = models.TimeField(verbose_name="Time", blank=True)
    end_time = models.TimeField(verbose_name="End Time", null=True)
    venue = models.CharField(max_length=512, verbose_name="Venue", blank=True)
    description = RichTextField(verbose_name="Description")
    meetup_location = models.ForeignKey(MeetupLocation, verbose_name="Meetup Location")
    created_by = models.ForeignKey(SystersUser, null=True, verbose_name="Created By")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Last Update")

    def __str__(self):
        return self.title


class RequestMeetup(models.Model):
    """Manage details of Meetup Requests of MeetupLocations"""
    title = models.CharField(max_length=50, verbose_name="Title",)
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Slug")
    date = models.DateField(verbose_name="Date")
    time = models.TimeField(verbose_name="Time", blank=True)
    venue = models.CharField(max_length=512, verbose_name="Venue", blank=True)
    description = RichTextField(verbose_name="Description")
    meetup_location = models.ForeignKey(MeetupLocation, verbose_name="Meetup Location")
    created_by = models.ForeignKey(SystersUser, null=True, verbose_name="Created By")
    approved_by = models.ForeignKey(SystersUser, blank=True, null=True,
                                    related_name='approvedBy')
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
    user = models.ForeignKey(SystersUser, verbose_name="User")
    meetup = models.ForeignKey(Meetup, verbose_name="Meetup")
    coming = models.BooleanField(default=True)
    plus_one = models.BooleanField(default=False)

    class Meta:
        unique_together = (('user', 'meetup'),)

    def __str__(self):
        return "{0} RSVP for meetup {1}".format(self.user, self.meetup)


class SupportRequest(models.Model):
    """Manage details of various volunteering activities"""
    volunteer = models.ForeignKey(SystersUser, verbose_name="Volunteer")
    meetup = models.ForeignKey(Meetup, verbose_name="Meetup")
    description = models.TextField(verbose_name="Description", blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return "{0} volunteered for meetup {1}".format(self.volunteer, self.meetup)
