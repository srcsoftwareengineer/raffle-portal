from django.db import models
from django.contrib.auth.models import User


class Raffle(models.Model):
    """
    @summary: Create relational entity 'raffles'
    """

    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    description = models.TextField()
    total_tickets = models.PositiveIntegerField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    draw_date = models.DateField()
    status = models.CharField(max_length=10, default="draft")

    def __str__(self):
        return f"{self.title} - {self.total_tickets} tickets"
