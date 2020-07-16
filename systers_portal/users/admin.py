from django.contrib import admin
from users.models import SystersUser, UserSetting


admin.site.register(SystersUser)
admin.site.register(UserSetting)
