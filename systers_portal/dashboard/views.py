from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from dashboard.models import SysterUser, Community, News, FAQ
from dashboard.forms import CommunityForm
from dashboard.forms import SysterUserForm, UserForm, UserEditForm
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test


def index(request):
    context = RequestContext(request)
    return render_to_response('dashboard/index.html', {}, context)


def profiles(request, user_name_url):
    context = RequestContext(request)
    user_name = user_name_url
    context_dic = {'user_name': user_name}
    try:
        user = User.objects.get(username=user_name)
        systeruser = SysterUser.objects.get(user=user)
        context_dic['user'] = user
        context_dic['systeruser'] = systeruser
    except User.DoesNotExist:
        pass
    return render_to_response('dashboard/profile.html', context_dic, context)


@login_required
def edit_profile(request):
    context = RequestContext(request)
    if request.method == 'POST':
        userform = UserEditForm(data=request.POST, instance=request.user)
        systeruserform = SysterUserForm(
            data=request.POST, instance=SysterUser.objects.get(user=request.user))
        if userform.is_valid() and systeruserform.is_valid():
            user = userform.save()
            systeruser = systeruserform.save(commit=False)
            if 'Profilepicture' in request.FILES:
                systeruser.Profilepicture = request.FILES['Profilepicture']
            systeruser.save()
            return HttpResponseRedirect('/dashboard/profile/' + user.username + '/')

        else:
            print userform.errors, systeruserform.errors
    else:
        userform = UserEditForm(instance=request.user)
        systeruserform = SysterUserForm(
            instance=SysterUser.objects.get(user=request.user))
    return render_to_response('dashboard/edit_profile.html', {'userform': userform, 'systeruserform': systeruserform}, context)


def community(request, community_name_url):
    context = RequestContext(request)
    community_name = community_name_url.replace('_', ' ')
    context_dic = {'community_name': community_name}
    try:
        community = Community.objects.get(name=community_name)
        members = SysterUser.objects.filter(community__name=community.name)
        context_dic['community'] = community
        context_dic['members'] = members
    except Community.DoesNotExist:
        pass
    return render_to_response('dashboard/community.html', context_dic, context)
