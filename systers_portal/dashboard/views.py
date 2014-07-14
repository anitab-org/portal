from django.shortcuts import render_to_response, get_object_or_404

from dashboard.models import Community


def view_community_profile(request, community_slug):
    """Display profile of a community

    :param request: request object
    :param community_slug: string slug parsed from the URL
    """
    community = get_object_or_404(Community, slug=community_slug)
    return render_to_response('dashboard/view_community_profile.html',
                              {'community': community})
