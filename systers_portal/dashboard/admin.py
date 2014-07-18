from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from dashboard.models import (
    SysterUser, Community, News, Resource, Tag, ResourceType,
    CommunityPage)


class CommunityAdmin(GuardedModelAdmin):
    pass


admin.site.register(SysterUser)
admin.site.register(Community, CommunityAdmin)
admin.site.register(News)
admin.site.register(Resource)
admin.site.register(Tag)
admin.site.register(ResourceType)
admin.site.register(CommunityPage)
