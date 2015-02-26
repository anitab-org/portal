from django import forms

from common.helpers import SubmitCancelFormHelper


class TransferOwnershipForm(forms.Form):
    """Form with a single field that allow a single choice out of a list of
    members of a community. Used to select the new admin of a community."""
    def __init__(self, *args, **kwargs):
        self.community = kwargs.pop('community')
        super(TransferOwnershipForm, self).__init__(*args, **kwargs)
        members = self.community.members.all()
        members = members.exclude(pk=self.community.admin.pk)
        choices = [(member.id, str(member)) for member in members]
        self.fields['new_admin'] = forms.ChoiceField(
            choices=choices, label="New community admin")

        self.helper = SubmitCancelFormHelper(
            self, cancel_href="{% url 'user' user.username %}")
