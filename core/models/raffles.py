# core/models/raffles.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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
    drawn_at = models.DateTimeField(null=True, blank=True)  # Hora real do sorteio
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.status})"


# class Raffle(models.Model):
#     """
#     @summary: Create relational entity 'raffles'
#     """
#
#     created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     total_tickets = models.PositiveIntegerField()
#     ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
#     draw_date = models.DateField()
#     # drawn_at = models.DateTimeField(null=True, blank=True)
#     status = models.CharField(max_length=10, default="draft")
#
#     def __str__(self):
#         return f"{self.title} - {self.total_tickets} tickets"
