from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext

from dashboard.models import Community, Resource


def show_community_resources(request, community_slug):
    """Show all resources of a community

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :raises Http404: if a community entry doesn't exist
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    resources = Resource.objects.filter(community=community)
    return render_to_response('dashboard/show_community_resources.html',
                              {'Resources': resources},
                              context)
