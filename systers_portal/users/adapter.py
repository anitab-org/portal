from allauth.account.adapter import DefaultAccountAdapter
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
import re


class SystersUserAccountAdapter(DefaultAccountAdapter):
    """Custom account adapter with different than default redirect URLs"""

    def clean_username(self, username, shallow=False):
        if len(username) < 3:
            raise ValidationError("Username must be atleast 3 characters long")

    def clean_password(self, password):
        # Password should have at least one uppercase letter , one digit and one special character
        x = r'^(?=.*?[A-Z])'
        y = '[~!@#$%^&*()_+{}":;\']+$'
        z = r'^(?=.*?[0-9])'
        digit = re.match(z, password)
        special_char = set(y).intersection(password)
        uppercase = re.match(x, password)
        if len(password) >= 6:
            if digit and uppercase and special_char:
                return password

            elif not digit and not uppercase and special_char:
                raise ValidationError(
                    "Password must have atleast one uppercase letter and one digit.")

            elif not special_char and not digit and uppercase:
                raise ValidationError(
                    "Password must have atleast one special character and one digit.")

            elif not special_char and not uppercase and digit:
                raise ValidationError(
                    "Password must have atleast one uppercase letter and one special character.")

            elif not special_char and digit and uppercase:
                raise ValidationError(
                    "Password must have atleast one special character")

            elif not uppercase and digit and special_char:
                raise ValidationError(
                    "Password must have atleast one uppercase letter")

            elif not digit and special_char and uppercase:
                raise ValidationError("Password must have atleast one digit")

            else:
                raise ValidationError(
                    "Password must have atleast one uppercase letter," +
                    " one special character and one digit")

        else:
            raise ValidationError("Password must have atleast 6 characters")

    def get_login_redirect_url(self, request):
        return reverse('user', args=[request.user.username])

    def get_signup_redirect_url(self, request):
        return reverse('user', args=[request.user.username])
