from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from community.models import Community, CommunityPage, JoinRequest


class CommunityAdmin(GuardedModelAdmin):
    def save_model(self, request, obj, form, change):
        """Override this method in order to be able to add the community admin
        to members list via admin panel."""
        members = list(form.cleaned_data['members'])
        members.extend([obj.community_admin])
        form.cleaned_data['members'] = members
        super(CommunityAdmin, self).save_model(request, obj, form, change)


admin.site.register(Community, CommunityAdmin)
admin.site.register(CommunityPage)
admin.site.register(JoinRequest)
