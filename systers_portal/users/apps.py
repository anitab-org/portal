from django.apps import AppConfig
from django.conf import settings


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals  # noqa # pylint: disable=unused-variable
        from . import scheduler
        if settings.SCHEDULER_AUTOSTART:
            scheduler.start()
