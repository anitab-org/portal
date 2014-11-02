from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Div, HTML

from users.models import SystersUser


class UserForm(forms.ModelForm):
    """User form combined with SystersUserForm"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance')
        systers_user = SystersUser.objects.get(user=user)
        systers_user_kwargs = kwargs.copy()
        systers_user_kwargs['instance'] = systers_user
        self.systers_user_form = SystersUserForm(*args, **systers_user_kwargs)

        super(UserForm, self).__init__(*args, **kwargs)

        self.fields.update(self.systers_user_form.fields)
        self.initial.update(self.systers_user_form.initial)

        # crispy FormHelper customization
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout.append(
            Div(
                Div(
                    HTML("""<a role="button" class="btn btn-default mr4"
                            href="{{ systersuser.get_absolute_url }}">
                            Cancel</a>"""),
                    Submit('save', 'submit', css_class='btn btn-primary'),
                    css_class='col-lg-9 col-lg-offset-3',
                ),
                css_class='form-group',
            ))

    def save(self, *args, **kwargs):
        self.systers_user_form.save(*args, **kwargs)
        return super(UserForm, self).save(*args, **kwargs)


class SystersUserForm(forms.ModelForm):
    """Form for SystersUser model"""
    class Meta:
        model = SystersUser
        fields = ('country', 'blog_url', 'homepage_url', 'profile_picture')
