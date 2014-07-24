from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from dashboard.forms import NewsForm
from dashboard.models import Community, SysterUser


def add_news(request, community_slug):
    """Add news for a community

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :raises Http404: if a community entry doesn't exist
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.community = community
            news.author = SysterUser.objects.get(user=request.user)
            news.save()
            return redirect('show_community_news',
                            community_slug=community.slug)
    else:
        form = NewsForm()
    return render_to_response('dashboard/add_news.html',
                              {'form': form, 'community': community},
                              context)
