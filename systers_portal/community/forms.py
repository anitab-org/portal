from django import forms
from django.contrib.auth.models import Group

from common.forms import ModelFormWithHelper
from common.helpers import SubmitCancelFormHelper
from community.constants import COMMUNITY_ADMIN
from community.models import Community, CommunityPage
from community.utils import get_groups
from users.models import SystersUser


class AddCommunityForm(ModelFormWithHelper):
    """ Form to create a new Community by admin. """
    class Meta:
        model = Community
        fields = ('name', 'slug', 'order', 'email', 'mailing_list',
                  'parent_community', 'website', 'facebook', 'googleplus',
                  'twitter')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'index' %}"

    def __init__(self, *args, **kwargs):
        self.admin = kwargs.pop('admin')
        super(AddCommunityForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """Override save to add admin to the instance"""
        instance = super(AddCommunityForm, self).save(commit=False)
        instance.admin = self.admin
        if commit:
            instance.save()
        return instance


class EditCommunityForm(ModelFormWithHelper):
    """Form to edit Community profile"""
    class Meta:
        model = Community
        fields = ('name', 'slug', 'order', 'email', 'mailing_list',
                  'parent_community', 'website', 'facebook', 'googleplus',
                  'twitter')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_community_profile' " \
                             "community.slug %}"


class AddCommunityPageForm(ModelFormWithHelper):
    """Form to create new CommunityPage. The author and the community of the
    page are expected to be provided when initializing the form:

    * author - currently logged in user, aka the author of the page
    * community - to which Community the CommunityPage belongs
    """
    class Meta:
        model = CommunityPage
        fields = ('title', 'slug', 'order', 'content')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_community_landing' " \
                             "community.slug %}"

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        self.community = kwargs.pop('community')
        super(AddCommunityPageForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """Override save to add author and community to the instance"""
        instance = super(AddCommunityPageForm, self).save(commit=False)
        instance.author = SystersUser.objects.get(user=self.author)
        instance.community = self.community
        if commit:
            instance.save()
        return instance


class EditCommunityPageForm(ModelFormWithHelper):
    """Form to edit a CommunityPage."""
    class Meta:
        model = CommunityPage
        fields = ('slug', 'title', 'order', 'content')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_community_page' community.slug " \
                             "object.slug %}"


class PermissionGroupsForm(forms.Form):
    """Form to manage (select/deselect) user permission groups"""
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        community = kwargs.pop('community')
        super(PermissionGroupsForm, self).__init__(*args, **kwargs)

        # get all community groups and remove community admin group
        # from the list of choices
        self.groups = list(get_groups(community.name))
        admin_group = Group.objects.get(
            name=COMMUNITY_ADMIN.format(community.name))
        self.groups.remove(admin_group)
        choices = [(group.pk, group.name) for group in self.groups]
        self.fields['groups'] = forms.\
            MultipleChoiceField(choices=choices, label="", required=False,
                                widget=forms.CheckboxSelectMultiple)
        self.member_groups = self.user.get_member_groups(self.groups)
        self.fields['groups'].initial = [group.pk for group in
                                         self.member_groups]

        self.helper = SubmitCancelFormHelper(
            self, cancel_href="{% url 'community_users' community.slug %}")

    def save(self):
        """Update the groups of which the user is member of"""
        group_pks = [int(pk) for pk in self.cleaned_data['groups']]
        for member_group in self.member_groups:
            if member_group.pk not in group_pks:
                self.user.leave_group(member_group)

        for pk in group_pks:
            group = Group.objects.get(pk=pk)
            if not self.user.is_group_member(group.name):
                self.user.join_group(group)
