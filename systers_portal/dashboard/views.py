from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from dashboard.models import SysterUser
from django.core.urlresolvers import reverse
from dashboard.forms import SysterUserForm
from dashboard.forms import UserForm


def index(request):
    context = RequestContext(request)
    return render_to_response('dashboard/index.html', {}, context)


def view_userprofile(request, username):
    context = RequestContext(request)
    context_dic = {'username': username}
    try:
        user = User.objects.get(username=username)
        systeruser = SysterUser.objects.get(user=user)
        context_dic['user'] = user
        context_dic['systeruser'] = systeruser
    except User.DoesNotExist:
        pass
    return render_to_response('dashboard/view_profile.html',
                              context_dic, context)


@login_required
def edit_userprofile(request, username):
    context = RequestContext(request)
    if request.method == 'POST':
        userform = UserForm(data=request.POST, instance=request.user)
        systeruserform = SysterUserForm(
            data=request.POST,
            instance=SysterUser.objects.get(user=request.user))
        if userform.is_valid() and systeruserform.is_valid():
            user = userform.save()
            systeruser = systeruserform.save(commit=False)
            if 'profile_picture' in request.FILES:
                systeruser.profile_picture = request.FILES['profile_picture']
            systeruser.save()
            return HttpResponseRedirect(
                reverse('view_userprofile', args=(user.username,)))
    else:
        userform = UserForm(instance=request.user)
        systeruserform = SysterUserForm(
            instance=SysterUser.objects.get(user=request.user))
    return render_to_response(
        'dashboard/edit_profile.html',
        {'userform': userform, 'systeruserform': systeruserform},
        context)
