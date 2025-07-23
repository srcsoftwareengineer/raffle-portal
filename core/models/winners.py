# core/models/winners.py

from django.db import models
from core.models.raffles import Raffle
from core.models.tickets import Ticket


class WinnerNotification(models.Model):
    """
    @summary: Create relational entity 'winners'
    """

    raffle = models.OneToOneField(Raffle, on_delete=models.DO_NOTHING)
    drawn_ticket = models.OneToOneField(Ticket, on_delete=models.DO_NOTHING)
    wapp_sent = models.BooleanField(default=False)
    wapp_sent_by = models.CharField(
        max_length=10,
        choices=[("System", "System"), ("User", "User")],
        null=True,
        blank=True,
        help_text="Indica se o envio foi manual ou automático",
    )

    @property
    def winner(self):
        return self.drawn_ticket.buyer

    def __str__(self):
        buyer = (
            self.drawn_ticket.buyer.username
            if self.drawn_ticket.buyer
            else "(sem comprador)"
        )
        return f"🏆 {buyer} venceu a rifa '{self.raffle.title}'"
