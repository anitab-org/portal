from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from dashboard.models import Community, News


def delete_news(request, community_slug, news_slug):
    """Ask Confirmation to delete news about a community

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :param news_slug: string news_slug parsed from the URL
    :raises Http404: if a community or news entry
                     inside community doesn't exist
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    news = get_object_or_404(News, community=community, slug=news_slug)
    return render_to_response('dashboard/delete_news.html',
                              {'news': news},
                              context)


def confirm_delete_news(request, community_slug, news_slug):
    """Delete news about a community after confirmation

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :param news_slug: string news_slug parsed from the URL
    :raises Http404: if a community or news entry
                     inside community doesn't exist
    """
    community = get_object_or_404(Community, slug=community_slug)
    news = get_object_or_404(News, community=community, slug=news_slug)
    news.delete()
    return redirect('show_community_news', community_slug=community.slug)
