from django.db import models
from django.contrib.auth.models import User
from django.db import models
from allauth.account.models import EmailAddress
from django.db.models.signals import post_save
from django_countries.fields import CountryField


class SysterUser(models.Model):

    """Profile model to store additional information about a user"""
    user = models.OneToOneField(User)
    country = CountryField(blank=True, null=True)
    BlogURL = models.URLField(max_length=255, blank=True, null=True)
    HomepageURL = models.URLField(max_length=255, blank=True, null=True)
    Profilepicture = models.ImageField(
        upload_to='photos/', default='photos/dummy.png', blank=True, null=True)

    def __unicode__(self):
        firstname = self.user.first_name
        lastname = self.user.last_name
        if firstname and lastname:
            return "{0} {1}".format(self.user.first_name, self.user.last_name)
        else:
            return self.user.username


def user_post_save(sender, instance, created, **kwargs):
    """Create a SysterUser profile when a new user account is created"""
    if created == True:
        systeruser = SysterUser()
        systeruser.user = instance
        systeruser.save()

post_save.connect(user_post_save, sender=User)


class Tag(models.Model):

    """Model to represent the tags a resource can have"""
    name = models.CharField(max_length=255, blank=False, null=False)

    def __unicode__(self):
        return self.name


class Community(models.Model):

    """Model to represent a Syster Community"""
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=255, blank=False, null=False)
    mailinglist = models.EmailField(max_length=255, blank=True, null=True)
    resourc_area = models.URLField(max_length=255, blank=True, null=True)
    members = models.ManyToManyField(SysterUser, blank=True, null=True)
    communityadmin = models.ForeignKey(User)
    website = models.URLField(max_length=30, blank=True, null=True)
    facebook = models.URLField(max_length=30, blank=True, null=True)
    googleplus = models.URLField(max_length=30, blank=True, null=True)
    twitter = models.URLField(max_length=30, blank=True, null=True)

    def __unicode__(self):
        return self.name


class News(models.Model):

    """Model to represent a News section on Community resource area"""

    title = models.CharField(max_length=255, blank=False, null=True)
    community = models.ForeignKey(Community)
    author = models.ForeignKey(SysterUser)
    date_created = models.DateField(auto_now=False, auto_now_add=True)
    date_modified = models.DateField(auto_now=True, auto_now_add=False)
    is_public = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    contents = models.TextField()

    def __unicode__(self):
        return "{0} of {0} Community".format(self.title, self.community.name)


class FAQ(models.Model):

    """Model to represent a FAQ section on Community resource area"""
    title = models.CharField(max_length=255, blank=False, null=True)
    community = models.ForeignKey(Community)
    author = models.ForeignKey(SysterUser)
    date_created = models.DateField(auto_now=False, auto_now_add=True)
    date_modified = models.DateField(auto_now=True, auto_now_add=False)
    contents = models.TextField()

    def __unicode__(self):
        return "{0} of {0} Community".format(self.title, self.community.name)


class Resource(models.Model):

    """Model to represent a Resources section on Community resource area"""
    RESOURCE_TYPES = (
        ('scholarship', 'Scholarship'),
        ('grant', 'Grant'),
        ('internship', 'Internship'),
        ('workshop', 'Workshop'),
        ('development', 'Professional Development'),
    )
    title = models.CharField(max_length=255, blank=False, null=False)
    community = models.ForeignKey(Community)
    author = models.ForeignKey(User)
    date_created = models.DateField(auto_now=False, auto_now_add=True)
    date_modified = models.DateField(auto_now=True, auto_now_add=False)
    is_public = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    contents = models.TextField()
    resource_type = models.CharField(max_length=30, choices=RESOURCE_TYPES)
