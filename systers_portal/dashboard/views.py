from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from dashboard.forms import ResourceForm
from dashboard.models import Community, SysterUser


def add_resource(request, community_slug):
    """Add resource for a community

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :raises Http404: if a community entry doesn't exist
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.community = community
            resource.author = SysterUser.objects.get(user=request.user)
            resource.save()
            return redirect('show_community_resources',
                            community_slug=community.slug)
    else:
        form = ResourceForm()
    return render_to_response('dashboard/add_resource.html',
                              {'form': form, 'community': community},
                              context)
