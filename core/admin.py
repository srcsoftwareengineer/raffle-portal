from django.contrib import admin
from core.models.winners import WinnerNotification


@admin.register(WinnerNotification)
class WinnerNotificationAdmin(admin.ModelAdmin):
    list_display = ("raffle", "winner", "timestamp", "wapp_sent")
    list_filter = ("wapp_sent",)
