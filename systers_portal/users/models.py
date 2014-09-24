from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
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
        firstname = self.user.first_name
        lastname = self.user.last_name
        if firstname and lastname:
            return "{0} {1}".format(firstname, lastname)
        else:
            return self.user.username


@receiver(post_save, sender=User)
def create_systers_user(sender, instance, created, **kwargs):
    """Keep User and SystersUser synchronized. Create a SystersUser instance on
    receiving a signal about new user signup.
    """
    if created:
        if instance is not None:
            systers_user = SystersUser(user=instance)
            systers_user.save()
