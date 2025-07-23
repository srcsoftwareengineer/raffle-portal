# core/models/raffles.py

from django.db import models
from django.contrib.auth.models import User


class Raffle(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("closed", "Closed"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    draw_date = models.DateField()
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2)
    total_tickets = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    create_date = models.DateField(auto_now_add=True)
    drawn_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    drawn_ticket = models.OneToOneField(
        "core.Ticket",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="won_raffle",
    )

    def __str__(self):
        return f"{self.title} ({self.status})"
