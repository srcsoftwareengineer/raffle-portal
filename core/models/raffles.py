from django.db import models
from django.contrib.auth.models import User


class Raffle(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_tickets = models.PositiveIntegerField(default=100)
    draw_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[
            ("draft", "Draft"),
            ("published", "Published"),
            ("finished", "Finished"),
        ],
        default="draft",
    )
    drawn_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.status})"
