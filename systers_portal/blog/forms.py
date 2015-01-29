from django import forms
from crispy_forms.helper import FormHelper

from common.crispy_forms.bootstrap import SubmitCancelFormActions
from blog.models import News, Resource
from users.models import SystersUser


class AddNewsForm(forms.ModelForm):
    """Form to add new Community News. The author and the community of the
     news should be provided by the view:

     * author - currently logged in user
     * community - defined by the community slug from the URL
     """
    class Meta:
        model = News
        fields = ['slug', 'title', 'content', 'is_public', 'is_monitored',
                  'tags']

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        self.community = kwargs.pop('community')
        super(AddNewsForm, self).__init__(*args, **kwargs)

        # crispy FormHelper customization
        self.helper = FormHelper(self)
        self.helper.layout.append(
            SubmitCancelFormActions(
                cancel_href="{% url 'view_community_news_list' "
                            "community.slug %}")
        )

    def save(self, commit=True):
        """Override save to add author and community to the instance."""
        instance = super(AddNewsForm, self).save(commit=False)
        instance.author = SystersUser.objects.get(user=self.author)
        instance.community = self.community
        if commit:
            instance.save()
        return instance


class EditNewsForm(forms.ModelForm):
    """Form to edit Community News."""
    class Meta:
        model = News
        fields = ['slug', 'title', 'content', 'is_public', 'is_monitored',
                  'tags']

    def __init__(self, *args, **kwargs):
        super(EditNewsForm, self).__init__(*args, **kwargs)

        # crispy FormHelper customization
        self.helper = FormHelper(self)
        self.helper.layout.append(
            SubmitCancelFormActions(
                cancel_href="{% url 'view_community_news' community.slug "
                            "object.slug %}")
        )


class AddResourceForm(forms.ModelForm):
    """Form to add new Community Resource. The author and the community of the
     resource should be provided by the view:

     * author - currently logged in user
     * community - defined by the community slug from the URL
     """
    class Meta:
        model = Resource
        fields = ['slug', 'title', 'content', 'is_public', 'is_monitored',
                  'tags', 'resource_type']

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        self.community = kwargs.pop('community')
        super(AddResourceForm, self).__init__(*args, **kwargs)

        # crispy FormHelper customization
        self.helper = FormHelper(self)
        self.helper.layout.append(
            SubmitCancelFormActions(
                cancel_href="{% url 'view_community_resource_list' "
                            "community.slug %}")
        )

    def save(self, commit=True):
        """Override save to add author and community to the instance."""
        instance = super(AddResourceForm, self).save(commit=False)
        instance.author = SystersUser.objects.get(user=self.author)
        instance.community = self.community
        if commit:
            instance.save()
        return instance


class EditResourceForm(forms.ModelForm):
    """Form to edit Community Resource."""
    class Meta:
        model = Resource
        fields = ['slug', 'title', 'content', 'is_public', 'is_monitored',
                  'tags', 'resource_type']

    def __init__(self, *args, **kwargs):
        super(EditResourceForm, self).__init__(*args, **kwargs)

        # crispy FormHelper customization
        self.helper = FormHelper(self)
        self.helper.layout.append(
            SubmitCancelFormActions(
                cancel_href="{% url 'view_community_resource' community.slug "
                            "object.slug %}")
        )
