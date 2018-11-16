from django.core.exceptions import ImproperlyConfigured


class MeetupLocationMixin(object):
    """Mixin to add information about MeetupLocation to context, as per the slug"""
    meetup_location = None

    def get_context_data(self, **kwargs):
        context = super(MeetupLocationMixin, self).get_context_data(**kwargs)
        context['meetup_location'] = self.get_meetup_location()
        return context

    def get_meetup_location(self):
        """Get a MeetupLocaiton object.

        :return: MeetupLocaiton object
        :raises ImproperlyConfigured: if MeetupLocaiton is set to None
        """
        if self.meetup_location is None:
            raise ImproperlyConfigured('{0} is missing a meetup_location. Define '
                                       '{0}.meetup_location or override {0}.get_meetup_location()'
                                       .format(self.__class__.__name__)
                                       )
