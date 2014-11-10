from django import forms
from crispy_forms.helper import FormHelper

from common.crispy_forms.bootstrap import SubmitCancelFormActions
from community.models import Community


class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ('name', 'slug', 'order', 'email', 'mailing_list',
                  'parent_community', 'website', 'facebook', 'googleplus',
                  'twitter')

    def __init__(self, *args, **kwargs):
        super(CommunityForm, self).__init__(*args, **kwargs)

        # crispy FormHelper customization
        self.helper = FormHelper(self)
        self.helper.layout.append(
            SubmitCancelFormActions(
                cancel_href="{% url 'view_community_profile' "
                            "community.slug %}")
        )
