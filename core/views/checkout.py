# core/views/checkout.py
"""
Created on 22 de jul. de 2025

@author: masterdev
"""
from django.shortcuts import get_object_or_404
from core.models.raffles import Raffle
from core.models.tickets import Ticket
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#
# @login_required
# def purchase_confirmation(request, raffle_id):
#     return render(request, "core/purchase_confirmation.html")


@login_required
def purchase_confirmation(request, raffle_id):
    raffle = get_object_or_404(Raffle, id=raffle_id)

    # Seleciona todos os tickets comprados pelo usuário nessa rifa
    purchased_tickets = Ticket.objects.filter(
        buyer=request.user, raffle=raffle
    ).order_by("number")

    return render(
        request,
        "core/purchase_confirmation.html",
        {
            "raffle": raffle,
            "purchased_tickets": purchased_tickets,
        },
    )
