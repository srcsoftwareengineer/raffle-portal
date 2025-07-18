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

    def __init__(self, *args, raffle=None, **kwargs):
        super().__init__(*args, **kwargs)
        if raffle:
            available = Ticket.objects.filter(raffle=raffle, buyer__isnull=True)
            self.fields["tickets"].choices = [(t.id, f"#{t.number}") for t in available]
