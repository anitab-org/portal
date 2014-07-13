from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext

from dashboard.models import SysterUser


def index(request):
    context = RequestContext(request)
    return render_to_response('dashboard/index.html', {}, context)


def view_userprofile(request, username):
    """View profile of a user

    :param request: request object
    :param username: string username parsed from the URL
    :raises Http404: if a user entry doesn't exist
    """
    context = RequestContext(request)
    user = get_object_or_404(User, username=username)
    systeruser = SysterUser.objects.get(user=user)
    return render_to_response('dashboard/view_profile.html',
                              {'systeruser': systeruser},
                              context)
