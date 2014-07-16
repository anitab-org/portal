from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from dashboard.forms import NewsForm
from dashboard.models import Community, News


def edit_news(request, community_slug, news_slug):
    """Edit a particluar news about a community

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :param news_slug: string news_slug parsed from the URL
    :raises Http404: if a community entry or news entry
    inside that community doesn't exist
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    news = get_object_or_404(News, community=community, slug=news_slug)
    if request.method == 'POST':
        newsform = NewsForm(request.POST, instance=news)
        if newsform.is_valid():
            changed_news = newsform.save()
            return redirect('view_news',
                            community_slug=community.slug,
                            news_slug=changed_news.slug)
        news = get_object_or_404(News, community=community, slug=news_slug)
    else:
            newsform = NewsForm(instance=news)
    return render_to_response('dashboard/edit_news.html',
                              {'newsform': newsform, 'news': news},
                              context)
