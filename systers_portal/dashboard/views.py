from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from guardian.decorators import permission_required_or_403

from dashboard.forms import CommunityForm
from dashboard.models import Community


@login_required
@permission_required_or_403('dashboard.change_community',
                            (Community, 'slug__exact', 'community_slug'))
def edit_community_profile(request, community_slug):
    """Edit profile of a community

    :param request: request object
    :param community_slug: string slug parsed from the URL
    :raises Http404: if a community entry doesn't exist
    :raises Http403: if user has no permissions to edit the community profile
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    if request.method == 'POST':
        form = CommunityForm(request.POST, instance=community)
        if form.is_valid():
            form.save()
            return redirect('view_community_profile',
                            community_slug=community.slug)
        community = get_object_or_404(Community, slug=community_slug)
    else:
        form = CommunityForm(instance=community)
    return render_to_response('dashboard/edit_community_profile.html',
                              {'form': form, 'community': community}, context)
