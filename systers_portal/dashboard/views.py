from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext

from dashboard.models import CommunityPage


def edit_page(request, community_slug, page_slug):
    page = get_object_or_404(CommunityPage, slug=page_slug)
    return render_to_response('page_template.html', {'page': page},
                              context_instance=RequestContext(request))
