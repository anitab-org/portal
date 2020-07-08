from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse
from django.core.exceptions import ValidationError
import re


class SystersUserAccountAdapter(DefaultAccountAdapter):
    """Custom account adapter with different than default redirect URLs"""

    def clean_username(self, username, shallow=False):
        if len(username) < 3:
            raise ValidationError("Username must be atleast 3 characters long")
        return username

    def clean_password(self, password, user=None):
        # Password should have at least one uppercase letter, one digit and one special character
        x = r'^(?=.*?[A-Z])'
        y = '[~!@#$%^&*()_+{}":;\']+$'
        z = r'^(?=.*?[0-9])'
        digit = re.match(z, password)
        special_char = set(y).intersection(password)
        uppercase = re.match(x, password)
        if len(password) >= 6 and digit and uppercase and special_char:
            return password
        else:
            raise ValidationError(
                "Password must have at least, 6 characters, one uppercase letter, "
                "one special character and one digit.")

    def get_login_redirect_url(self, request):
        return reverse('user', args=[request.user.username])

    def get_signup_redirect_url(self, request):
        return reverse('user', args=[request.user.username])
