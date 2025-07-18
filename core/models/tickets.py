from django.db import models
from django.contrib.auth.models import User
from .raffles import Raffle


class Ticket(models.Model):
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    buyer = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)
    STATUS_CHOICES = [
        ("available", "Available"),
        ("reserved", "Reserved"),
        ("sold", "Sold"),
    ]
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="available"
    )

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return f"Ticket #{self.number} - {self.status}"
