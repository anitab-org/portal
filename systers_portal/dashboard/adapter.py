from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.shortcuts import resolve_url
from datetime import datetime, timedelta


class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        if request.user.is_authenticated():
            url = '/dashboard/profile/' + request.user.username + '/'
        return resolve_url(url)

    def get_signup_redirect_url(self, request):
        if request.user.is_authenticated():
            url = '/dashboard/profile/' + request.user.username + '/'
        return resolve_url(url)
