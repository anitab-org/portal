from django.db.models.signals import post_save
from django.dispatch import receiver

from community.models import Community


@receiver(post_save, sender=Community, dispatch_uid="create_groups")
def manage_community_groups(sender, instance, created, **kwargs):
    """Create user groups for a particular Community instance and assign
    permissions to each group"""
    pass
