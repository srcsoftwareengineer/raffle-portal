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
def list_raffles(request):
    user_raffles = Raffle.objects.filter(created_by=request.user)
    raffles_with_tickets = []

    for raffle in user_raffles:
        tickets = Ticket.objects.filter(raffle=raffle, buyer__isnull=True).count()
        raffles_with_tickets.append({"raffle": raffle, "available_tickets": tickets})
    return render(
        request,
        "core/list_raffles.html",
        {"raffles_with_tickets": raffles_with_tickets},
    )
