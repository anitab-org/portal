from allauth.account.adapter import DefaultAccountAdapter
from django.core.urlresolvers import reverse
from django.shortcuts import resolve_url


class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        if request.user.is_authenticated():
            url = reverse('view_userprofile', args=[request.user.username])
        return resolve_url(url)

    def get_signup_redirect_url(self, request):
        if request.user.is_authenticated():
            url = reverse('view_userprofile', args=[request.user.username])
        return resolve_url(url)
