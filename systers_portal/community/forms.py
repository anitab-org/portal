from django import forms
from crispy_forms.helper import FormHelper

from common.crispy_forms.bootstrap import SubmitCancelFormActions
from community.models import Community, CommunityPage
from users.models import SystersUser


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


class AddCommunityPageForm(forms.ModelForm):
    """Form to create new CommunityPage. The author and the community of the
    page are expected to be provided when initializing the form:

    * author - currently logged in user, aka the author of the page
    * community - to which Community the CommunityPage belongs
    """
    class Meta:
        model = CommunityPage
        fields = ('slug', 'title', 'order', 'content')

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        self.community = kwargs.pop('community')
        super(AddCommunityPageForm, self).__init__(*args, **kwargs)

        # crispy FormHelper customization
        self.helper = FormHelper(self)
        self.helper.layout.append(
            SubmitCancelFormActions(
                cancel_href="{% url 'view_community_landing' "
                            "community.slug %}")
        )

    def save(self, commit=True):
        """Override save to add author and community to the instance"""
        instance = super(AddCommunityPageForm, self).save(commit=False)
        instance.author = SystersUser.objects.get(user=self.author)
        instance.community = self.community
        if commit:
            instance.save()
        return instance


class EditCommunityPageForm(forms.ModelForm):
    """For to edit a CommunityPage."""
    class Meta:
        model = CommunityPage
        fields = ('slug', 'title', 'order', 'content')

    def __init__(self, *args, **kwargs):
        super(EditCommunityPageForm, self).__init__(*args, **kwargs)

        # crispy FormHelper customization
        self.helper = FormHelper(self)
        self.helper.layout.append(
            SubmitCancelFormActions(
                cancel_href="{% url 'view_community_page' community.slug "
                            "object.slug %}")
        )
