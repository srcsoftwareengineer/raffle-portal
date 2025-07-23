# core/models/tickets.py

from django.db import models
from django.contrib.auth.models import User
from .raffles import Raffle


class Ticket(models.Model):
    """
    @summary: Create relational entity 'tickets'
    """

    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE, related_name="tickets")
    number = models.PositiveIntegerField()
    buyer = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="tickets_purchased",
    )
    is_reserved = models.BooleanField(default=False)
    payment_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Ticket #{self.number} for Raffle {self.raffle.id}"
