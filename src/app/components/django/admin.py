from django.contrib.admin import AdminSite as BaseAdminSite
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin, GroupAdmin, User, Group


class AdminSite(BaseAdminSite):
    site_title = _('App Admin')
    site_header = _('App Admin')


admin = AdminSite()
admin.register(User, UserAdmin)
admin.register(Group, GroupAdmin)
