from common.forms import ModelFormWithHelper
from common.helpers import SubmitCancelFormHelper
from blog.models import News, Resource, Tag, ResourceType
from users.models import SystersUser


class AddNewsForm(ModelFormWithHelper):
    """Form to add new Community News. The author and the community of the
     news should be provided by the view:

     * author - currently logged in user
     * community - defined by the community slug from the URL
     """
    class Meta:
        model = News
        fields = ['slug', 'title', 'content', 'is_public', 'is_monitored',
                  'tags']
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_community_news_list' " \
                             "community.slug %}"

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        self.community = kwargs.pop('community')
        super(AddNewsForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """Override save to add author and community to the instance."""
        instance = super(AddNewsForm, self).save(commit=False)
        instance.author = SystersUser.objects.get(user=self.author)
        instance.community = self.community
        if commit:
            instance.save()
        return instance


class EditNewsForm(ModelFormWithHelper):
    """Form to edit Community News."""
    class Meta:
        model = News
        fields = ['slug', 'title', 'content', 'is_public', 'is_monitored',
                  'tags']
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_community_news' community.slug " \
                             "object.slug %}"


class AddResourceForm(ModelFormWithHelper):
    """Form to add new Community Resource. The author and the community of the
     resource should be provided by the view:

     * author - currently logged in user
     * community - defined by the community slug from the URL
     """
    class Meta:
        model = Resource
        fields = ['slug', 'title', 'content', 'is_public', 'is_monitored',
                  'tags', 'resource_type']
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_community_resource_list' " \
                             "community.slug %}"

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        self.community = kwargs.pop('community')
        super(AddResourceForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """Override save to add author and community to the instance."""
        instance = super(AddResourceForm, self).save(commit=False)
        instance.author = SystersUser.objects.get(user=self.author)
        instance.community = self.community
        if commit:
            instance.save()
        return instance


class EditResourceForm(ModelFormWithHelper):
    """Form to edit Community Resource."""
    class Meta:
        model = Resource
        fields = ['slug', 'title', 'content', 'is_public', 'is_monitored',
                  'tags', 'resource_type']
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_community_resource' " \
                             "community.slug object.slug %}"


class TagForm(ModelFormWithHelper):
    """Form to create or edit a tag"""
    class Meta:
        model = Tag
        fields = ['name']
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_community_news_list' " \
                             "community.slug %}"


class ResourceTypeForm(ModelFormWithHelper):
    """Form to create or edit a ResourceType object"""
    class Meta:
        model = ResourceType
        fields = ['name']
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_community_resource_list' " \
                             "community.slug %}"
