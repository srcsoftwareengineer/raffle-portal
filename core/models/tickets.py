# core/models/tickets.py

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["raffle", "number"], name="uniq_ticket_per_raffle"
            ),
        ]
        ordering = ["number"]

    def clean(self):
        # Garante que o número está no range da rifa
        if self.raffle_id and self.number:
            if not (1 <= self.number <= self.raffle.total_tickets):
                raise ValidationError(
                    {
                        "number": f"Número precisa estar entre 1 e {self.raffle.total_tickets}."
                    }
                )

    def __str__(self):
        return f"Ticket #{self.number} for Raffle {self.raffle.id}"
