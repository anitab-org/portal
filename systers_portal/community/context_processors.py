from community.models import Community


def communities_processor(request):
    """Custom template context preprocessor that allows to inject into every
    request the list of all communities. This is necessary in order to display
    the list of communities in the navigation bar."""
    communities = Community.objects.all().order_by("order")
    return {'communities': communities}
