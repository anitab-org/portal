from blog.models import ResourceType


class ResourceTypesMixin(object):
    """Mixin allows to add to the context all resource type object"""
    def get_context_data(self, **kwargs):
        context = super(ResourceTypesMixin, self).get_context_data(**kwargs)
        context["resource_types"] = ResourceType.objects.all()
        return context
