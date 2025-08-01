# core/models/raffles.py

from django.db import models, transaction
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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    drawn_ticket = models.OneToOneField(
        "core.Ticket",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="won_raffle",
    )

    def __str__(self):
        return f"{self.title} ({self.status})"

    @transaction.atomic
    def generate_missing_tickets(self):
        """
        Cria os tickets que faltam no range 1..total_tickets.
        Não recria os que já existem.
        """
        from .tickets import Ticket

        # Pega números já existentes
        existing = set(self.tickets.values_list("number", flat=True))
        to_create = [
            Ticket(raffle=self, number=n)
            for n in range(1, self.total_tickets + 1)
            if n not in existing
        ]
        if to_create:
            Ticket.objects.bulk_create(to_create, batch_size=1000)

    def sold_count(self):
        return self.tickets.filter(payment_confirmed=True).count()

    def remaining_queryset(self):
        # “Restantes” aqui significa “sem comprador confirmado”
        return self.tickets.filter(payment_confirmed=False)

    @transaction.atomic
    def buy_remaining(
        self, buyer: User, confirm_payment: bool = True, reserve: bool = False
    ):
        """
        Atribui todos os tickets NÃO pagos ao usuário 'buyer'.
        Opcionalmente confirma pagamento.
        """
        qs = self.remaining_queryset().select_for_update()
        qs.update(buyer=buyer, payment_confirmed=confirm_payment, is_reserved=reserve)
        return qs.count()
