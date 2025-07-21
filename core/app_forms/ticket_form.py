# core/forms/ticket_form.py
"""
Created on 18 de jul. de 2025

@author: masterdev
"""

from django import forms
from core.models.tickets import Ticket


class TicketPurchaseForm(forms.Form):
    tickets = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[],  # dynamically filled in view
        label="Select tickets",
    )

    def _get_available_tickets(self, raffle: object):
        def fill_tickets_choices():
            self.fields["tickets"].choices = [
                (t.id, f"Nº {t.number}") for t in available_numbers
            ]

        def create_tickets():
            assert raffle.total_tickets > 0
            idx: int = raffle.total_tickets
            while idx > 0:
                Ticket.objects.create(
                    raffle=raffle, number=idx, buyer_id=None, is_reserved=False
                )
                idx -= 1
            fill_tickets_choices()

        available_numbers = Ticket.objects.filter(raffle=raffle.id, buyer__isnull=True)
        if available_numbers.exists():
            fill_tickets_choices()
        else:
            create_tickets()

    def get_available_tickets(self, raffle: object) -> list:
        self._get_available_tickets(raffle)
        return self.fields["tickets"].choices

    def __init__(self, *args, raffle=None, **kwargs):
        super().__init__(*args, **kwargs)
        if raffle:
            self.get_available_tickets(raffle)
        return
