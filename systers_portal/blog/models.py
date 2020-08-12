from django.urls import reverse
from django.db import models

from common.models import Post
from community.models import Community

from users.models import SystersUser


class Tag(models.Model):
    """Model to represent the tags news or resource can have"""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class ResourceType(models.Model):
    """Model to represent the types a resource can have"""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class News(Post):
    """Model to represent community news in resource area"""
    community = models.ForeignKey(Community, verbose_name="Community", on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True, verbose_name="Is public")
    is_monitored = models.BooleanField(default=False,
                                       verbose_name="Is monitored")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Tags")

    class Meta:
        verbose_name_plural = "News"
        unique_together = ('community', 'slug')

    def __str__(self):
        return "{0} of {1} Community".format(self.title, self.community.name)

    def get_absolute_url(self):
        """Absolute URL to a News object"""
        return reverse('view_community_news',
                       kwargs={'slug': self.community.slug,
                               'news_slug': self.slug})


class Resource(Post):
    """Model to represent community resource in resource area"""
    community = models.ForeignKey(Community, verbose_name="Community", on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True, verbose_name="Is public")
    is_monitored = models.BooleanField(default=False,
                                       verbose_name="Is monitored")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Tags")
    resource_type = models.ForeignKey(ResourceType, blank=True, null=True,
                                      verbose_name="Resource type", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('community', 'slug')

    def __str__(self):
        return "{0} of {1} Community".format(self.title, self.community.name)

    def get_absolute_url(self):
        """Absolute URL to a Resource object"""
        return reverse('view_community_resource',
                       kwargs={'slug': self.community.slug,
                               'resource_slug': self.slug})


class UserPins(models.Model):
    user = models.OneToOneField(SystersUser, on_delete=models.CASCADE)
    pins = models.ManyToManyField(Resource, blank=True, related_name="pins", verbose_name="pins")

    def __str__(self):
        return "Pins for {0}".format(self.user)

    def add_pin(self, resource):
        self.pins.add(resource)

    def remove_pin(self, resource):
        self.pins.remove(resource)
