from django.contrib import admin
from core.models.winners import WinnerNotification


@admin.register(WinnerNotification)
class WinnerNotificationAdmin(admin.ModelAdmin):
    list_display = ("raffle", "winner", "wapp_sent")
    list_filter = ("wapp_sent",)


# DEVTOOLS
# from django.contrib.auth.models import Group, User
#
# group, created = Group.objects.get_or_create(name="super-admin")
# admin_user = User.objects.get(username="admin")
# admin_user.groups.add(group)
