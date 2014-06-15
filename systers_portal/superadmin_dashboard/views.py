from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from dashboard.models import SysterUser, Community, News, FAQ
from superadmin_dashboard.forms import CommunityForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
"""@user_passes_test(lambda u: u.is_superuser)"""
def index(request):
    context = RequestContext(request)
    community_list = Community.objects.all()
    context_dic = {'communities': community_list}
    for community in community_list:
        community.url = community.name.replace(' ', '_')
    return render_to_response('superadmin_dashboard/index.html', context_dic, context)

def ShowCommunities(request):
    context = RequestContext(request)
    community_list = Community.objects.all()
    context_dic = {'communities': community_list}
    for community in community_list:
        community.url = community.name.replace(' ', '_')
    return render_to_response('superadmin_dashboard/show_communities.html', context_dic, context)

def add_community(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = CommunityForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = CommunityForm()
    return render_to_response('superadmin_dashboard/add_community.html', {'form': form}, context)


def edit_communityprofile(request, community_name_url):
    context = RequestContext(request)
    community_name = community_name_url.replace('_', ' ')
    context_dic = {'community_name': community_name}
    context_dic ['community_name_url']=community_name_url
    try:
        community = Community.objects.get(name=community_name)
        context_dic["community"] = community
        if request.method == 'POST':
            communityform = CommunityForm(
                data=request.POST, instance=community)
            context_dic['communityform'] = communityform
            if communityform.is_valid():
                community = communityform.save()
            	return index(request)
            else:
                print communityform.errors
        else:
            communityform = CommunityForm(instance=community)
            context_dic['communityform'] = communityform

    except Community.DoesNotExist:
        pass

    return render_to_response('superadmin_dashboard/edit_communityprofile.html', context_dic, context)
