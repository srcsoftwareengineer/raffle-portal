from django.db import models
from django.contrib.auth.models import User
from core.models.raffles import Raffle


class Ticket(models.Model):
    raffle = models.ForeignKey(Raffle, on_delete=models.PROTECT)
    buyer = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    number = models.PositiveIntegerField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_confirmed = models.BooleanField(default=False)
