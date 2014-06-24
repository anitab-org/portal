from django.contrib import admin
from dashboard.models import SysterUser
from dashboard.models import Community
from dashboard.models import News
from dashboard.models import Resource
from dashboard.models import Tag
from dashboard.models import Resource_Type
from dashboard.models import CommunityPages

admin.site.register(SysterUser)
admin.site.register(Community)
admin.site.register(News)
admin.site.register(Resource)
admin.site.register(Tag)
admin.site.register(Resource_Type)
admin.site.register(CommunityPages)
