from django.db import models
from django.contrib.auth.models import User
from core.models.raffles import Raffle


class WinnerNotification(models.Model):
    raffle = models.OneToOneField(Raffle, on_delete=models.DO_NOTHING)
    winner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    mobile_prefix = models.PositiveIntegerField()
    mobile_number = models.CharField(max_length=11)
    notified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Winner for {self.raffle.title} is {self.winner.username}"
