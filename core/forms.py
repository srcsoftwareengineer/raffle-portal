"""
Created on 15 de jul. de 2025

@author: Sandro Regis Cardoso
"""

from django import forms
from core.models.raffles import Raffle


class RaffleForm(forms.ModelForm):

    class Meta:
        model = Raffle
        fields = [
            "title",
            "description",
            "draw_date",
            "ticket_price",
            "total_tickets",
            "status",
        ]
        widgets = {
            "draw_date": forms.DateInput(attrs={"type": "date"}),
        }


class PurchaseTicketForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label="Quantidade de Tickets")
