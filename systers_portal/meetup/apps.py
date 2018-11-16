from django.apps import AppConfig


class MeetupConfig(AppConfig):
    name = 'meetup'

    def ready(self):
        import meetup.signals  # noqa # pylint: disable=unused-variable
