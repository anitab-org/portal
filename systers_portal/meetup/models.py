from django.db import models
from ckeditor.fields import RichTextField
from cities_light.models import City

from users.models import SystersUser


class MeetupLocation(models.Model):
    """Manage details of Meetup Location groups"""
    name = models.CharField(max_length=255, unique=True, verbose_name="Name")
    slug = models.SlugField(max_length=150, unique=True, verbose_name="Slug")
    location = models.ForeignKey(City, verbose_name="Location")
    description = RichTextField(verbose_name="Description")
    email = models.EmailField(max_length=255, blank=True, verbose_name="Email")
    organizers = models.ManyToManyField(SystersUser,
                                        related_name="Organizers",
                                        verbose_name="Organizers")
    members = models.ManyToManyField(SystersUser, blank=True,
                                     related_name="Members",
                                     verbose_name="Members")

    def __str__(self):
        return "{0} Systers".format(self.name)
