from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from dashboard.forms import ResourceForm
from dashboard.models import Community, Resource, SysterUser


def edit_resource(request, community_slug, resource_slug):
    """Edit a particluar resource of a community

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
    if request.method == 'POST':
        resourceform = ResourceForm(request.POST, instance=resource)
        if resourceform.is_valid():
            changed_resource = resourceform.save()
            return redirect('view_resource',
                            community_slug=community.slug,
                            resource_slug=changed_resource.slug)
        resource = get_object_or_404(Resource,
                                     community=community,
                                     slug=resource_slug)
    else:
            resourceform = ResourceForm(instance=resource)
    return render_to_response('dashboard/edit_resource.html',
                              {'resourceform': resourceform,
                               'resource': resource},
                              context)
