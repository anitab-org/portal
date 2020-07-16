from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import SystersUser, UserSetting


@receiver(post_save, sender=SystersUser, dispatch_uid="create_settings")
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        UserSetting.objects.create(user=instance)
