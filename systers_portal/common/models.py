from django.db import models

from users.models import SystersUser


class Post(models.Model):
    """Abstract base class for postings like news and resources.
    This class can't be used in isolation.
    """
    slug = models.SlugField(max_length=150, unique=True, verbose_name="Slug")
    title = models.CharField(max_length=255, verbose_name="Title")
    date_created = models.DateField(auto_now=False, auto_now_add=True,
                                    verbose_name="Date published")
    date_modified = models.DateField(auto_now=True, auto_now_add=False,
                                     verbose_name="Date last modified")
    author = models.ForeignKey(SystersUser, verbose_name="Author")
    content = models.TextField(verbose_name="Content")

    class Meta:
        abstract = True
