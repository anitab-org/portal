from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField


class SystersUser(models.Model):
    """Profile model to store additional information about a user"""
    user = models.OneToOneField(User)
    country = CountryField(blank=True, null=True, verbose_name="Country")
    blog_url = models.URLField(max_length=255, blank=True, verbose_name="Blog")
    homepage_url = models.URLField(max_length=255, blank=True,
                                   verbose_name="Homepage")
    profile_picture = models.ImageField(upload_to='users/pictures/',
                                        blank=True,
                                        null=True,
                                        verbose_name="Profile picture")

    def __unicode__(self):
        return unicode(self.user)

    def get_absolute_url(self):
        """Absolute URL to a SystersUser object"""
        return reverse('user', kwargs={'username': self.user.username})

    def join_group(self, group):
        """Make user member of a group

        :param group: Group object
        """
        group.user_set.add(self.user)

    def leave_group(self, group):
        """Remove user from group members

        :param group: Group object
        """
        group.user_set.remove(self.user)

    def get_fields(self):
        """Get model fields of a SystersUser object

        :return: list of tuples (fieldname, fieldvalue)
        """
        return [(field.name, getattr(self, field.name)) for field in
                SystersUser._meta.fields]

    def is_member(self, community):
        """Check if the user is a member of the community

        :param community: Community object
        :return: True if user is member of the community, False otherwise
        """
        return self.communities.filter(pk=community.pk).exists()

    def get_last_join_request(self, community):
        """Get the last join request made by the user to a community

        :param community: Community object
        :return: JoinRequest object or None in case user has made no requests
        """
        from community.models import JoinRequest
        join_requests = JoinRequest.objects.filter(user=self,
                                                   community=community).\
            order_by('-date_created')
        if join_requests:
            return join_requests[0]

    def approve_all_join_requests(self, community):
        """Approve all join requests of a user towards a community.

        :param community: Community object
        """
        from community.models import JoinRequest
        join_requests = JoinRequest.objects.filter(user=self,
                                                   community=community,
                                                   is_approved=False)
        for join_request in join_requests:
            join_request.approve()


def user_unicode(self):
    """Unicode representation of Django User model

    :return: string User name
    """
    firstname = self.first_name
    lastname = self.last_name
    if firstname and lastname:
        return "{0} {1}".format(firstname, lastname)
    else:
        return self.username


# Overriding the unicode representation of Django User model
User.__unicode__ = user_unicode


@receiver(post_save, sender=User)
def create_systers_user(sender, instance, created, **kwargs):
    """Keep User and SystersUser synchronized. Create a SystersUser instance on
    receiving a signal about new user signup.
    """
    if created:
        if instance is not None:
            systers_user = SystersUser(user=instance)
            systers_user.save()
