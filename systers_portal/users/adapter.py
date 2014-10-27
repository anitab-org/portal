from allauth.account.adapter import DefaultAccountAdapter
from django.core.urlresolvers import reverse


class SystersUserAccountAdapter(DefaultAccountAdapter):
    """Custom account adapter with different than default redirect URLs"""
    def get_login_redirect_url(self, request):
        return reverse('user_profile', args=[request.user.username])

    def get_signup_redirect_url(self, request):
        return reverse('user_profile', args=[request.user.username])
