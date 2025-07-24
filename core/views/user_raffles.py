# core/views/user_raffles.py
"""
Created on 21 de jul. de 2025

@author: masterdev
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.models.raffles import Raffle
from core.models.tickets import Ticket


@login_required
def list_user_raffles(request):
    available_tickets: dict = {}
    user_raffles = Raffle.objects.filter(
        created_by=request.user
    )  # List only the raffles created by logged user
    for raffle in user_raffles:
        tickets = Ticket.objects.filter(raffle=raffle.id, buyer__isnull=True).count()
        available_tickets.update(
            {"raffles": user_raffles, "available_tickets": tickets}
        )
    return render(request, "core/list_raffles.html", available_tickets)
