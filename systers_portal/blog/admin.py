from django.contrib import admin

from blog.models import (Tag, ResourceType, News, Resource)


admin.site.register(Tag)
admin.site.register(ResourceType)
admin.site.register(News)
admin.site.register(Resource)
