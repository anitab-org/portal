from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext

from dashboard.models import Community, Resource


def view_resource(request, community_slug, resource_slug):
    """View a particluar resource of a community

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :param resource_slug: string resource_slug parsed from the URL
    :raises Http404: if a community entry or resource entry
                     inside that community doesn't exist
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    resource = get_object_or_404(Resource,
                                 community=community,
                                 slug=resource_slug)
    return render_to_response('dashboard/view_resource.html',
                              {'resource': resource},
                              context)
