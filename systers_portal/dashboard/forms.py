from django.forms import ModelForm

from dashboard.models import Community


class CommunityForm(ModelForm):
    """Community profile form excluding the members ManyToManyField
    """
    class Meta:
        model = Community
        exclude = ['members']
