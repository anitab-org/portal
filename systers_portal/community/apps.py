from django.apps import AppConfig


class CommunityConfig(AppConfig):
    name = 'community'

    def ready(self):
        import community.signals  # noqa # pylint: disable=unused-variable
