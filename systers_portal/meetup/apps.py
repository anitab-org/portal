from django.apps import AppConfig


class MeetupConfig(AppConfig):
    name = 'meetup'

    def ready(self):
        import meetup.signals
        assert meetup.signals
