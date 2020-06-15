from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import Group

from common.forms import ModelFormWithHelper
from common.helpers import SubmitCancelFormHelper
from community.constants import COMMUNITY_ADMIN, COMMUNITY_PRESENCE_CHOICES
from community.models import Community, CommunityPage, RequestCommunity
from community.utils import get_groups
from users.models import SystersUser


class AddCommunityForm(ModelFormWithHelper):
    """ Form to create a new Community by admin. """

    class Meta:
        model = Community
        fields = ('name', 'slug', 'order', 'location', 'email', 'mailing_list',
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


class RequestCommunityForm(ModelFormWithHelper):
    """Form to request a new Community"""

    def __init__(self, *args, **kwargs):
        """Makes some fields required and modifies a field to use widget"""
        self.user = kwargs.pop('user')
        super(RequestCommunityForm, self).__init__(*args, **kwargs)
        self.fields['social_presence'] = forms.MultipleChoiceField(
            choices=COMMUNITY_PRESENCE_CHOICES, label="Check off all \
            the social media accounts you can manage for your proposed community:",
            required=False, widget=forms.CheckboxSelectMultiple)
        self.fields['email'].required = True
        self.fields['demographic_target_count'].required = True
        self.fields['purpose'].required = True
        self.fields['content_developer'].required = True
        self.fields['selection_criteria'].required = True
        self.fields['is_real_time'].required = True

    class Meta:
        model = RequestCommunity
        fields = ('is_member', 'email_id', 'email', 'name', 'slug', 'order', 'location',
                  'type_community', 'other_community_type', 'parent_community',
                  'community_channel', 'mailing_list', 'website', 'facebook',
                  'googleplus', 'twitter', 'social_presence', 'other_account',
                  'demographic_target_count',
                  'purpose', 'is_avail_volunteer', 'count_avail_volunteer', 'content_developer',
                  'selection_criteria', 'is_real_time')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'index' %}"

    def clean_social_presence(self):
        """Converts the checkbox input into char to save it to the instance's field."""
        social_presence = ', '.join(
            map(str, self.cleaned_data['social_presence']))
        return social_presence

    def save(self, commit=True):
        """Override save to add user to the instance"""
        instance = super(RequestCommunityForm, self).save(commit=False)
        instance.user = SystersUser.objects.get(user=self.user)
        if commit:
            instance.save()
        return instance


class EditCommunityRequestForm(ModelFormWithHelper):
    """Form to edit a community request"""

    def __init__(self, *args, **kwargs):
        """Makes some fields required and modifies a field to use widget"""
        super(EditCommunityRequestForm, self).__init__(*args, **kwargs)
        self.fields['social_presence'] = forms.MultipleChoiceField(
            choices=COMMUNITY_PRESENCE_CHOICES, label="Check off all \
            the social media accounts you can manage for your proposed community:",
            required=False, widget=forms.CheckboxSelectMultiple)
        self.fields['email'].required = True
        self.fields['demographic_target_count'].required = True
        self.fields['purpose'].required = True
        self.fields['content_developer'].required = True
        self.fields['selection_criteria'].required = True
        self.fields['is_real_time'].required = True

    class Meta:
        model = RequestCommunity
        fields = ('is_member', 'email_id', 'email', 'name', 'slug', 'order', 'location',
                  'type_community', 'other_community_type', 'parent_community',
                  'community_channel', 'mailing_list', 'website', 'facebook',
                  'googleplus', 'twitter', 'social_presence', 'other_account',
                  'demographic_target_count',
                  'purpose', 'is_avail_volunteer', 'count_avail_volunteer', 'content_developer',
                  'selection_criteria', 'is_real_time')
        widgets = {'social_presence': forms.CheckboxSelectMultiple}
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_community_request' community_request.slug %}"

    def clean_social_presence(self):
        """Converts the checkbox input into char to save it to the instance's field."""
        social_presence = ', '.join(
            map(str, self.cleaned_data['social_presence']))
        return social_presence

    def clean_slug(self):
        """Checks if the slug exists in the Community objects' slug"""
        slug = self.cleaned_data['slug']
        slug_community_values = Community.objects.all().values_list('order', flat=True)
        if slug in slug_community_values:
            msg = "Slug by this value already exists. Please choose a different slug\
                   other than {0}!"
            string_slug_values = ', '.join(map(str, slug_community_values))
            raise ValidationError(msg.format(string_slug_values))
        else:
            return slug

    def clean_order(self):
        """Checks if the order exists in the Community objects' order"""
        order = self.cleaned_data['order']
        order_community_values = list(
            Community.objects.all().values_list('order', flat=True))
        order_community_values.sort()
        if order is None:
            raise ValidationError("Order must not be None.")
        elif order in order_community_values:
            msg = "Choose order value other than {0}"
            string_order_values = ', '.join(map(str, order_community_values))
            raise ValidationError(msg.format(string_order_values))
        else:
            return order


class EditCommunityForm(ModelFormWithHelper):
    """Form to edit Community profile"""

    class Meta:
        model = Community
        fields = ('name', 'slug', 'order', 'location', 'email', 'mailing_list',
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
        self.fields['groups'] = forms. \
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
