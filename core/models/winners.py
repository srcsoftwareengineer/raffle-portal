from django.db import models
from django.contrib.auth.models import User
from .raffles import Raffle


class WinnerNotification(models.Model):
    raffle = models.OneToOneField(Raffle, on_delete=models.DO_NOTHING)
    winner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    winner_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Winner of {self.raffle.title}: {self.winner.username}"
