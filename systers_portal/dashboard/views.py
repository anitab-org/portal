from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext

from dashboard.models import Community, News


def view_news(request, community_slug, news_slug):
    """View a particluar news about a community

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :param news_slug: string news_slug parsed from the URL
    :raises Http404: if a community entry or news entry
                     inside that community doesn't exist
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    news = get_object_or_404(News, community=community, slug=news_slug)
    return render_to_response('dashboard/view_news.html',
                              {'news': news},
                              context)
