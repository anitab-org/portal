from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from community.models import Community, CommunityPage


class CommunityAdmin(GuardedModelAdmin):
    pass


admin.site.register(Community, CommunityAdmin)
admin.site.register(CommunityPage)
