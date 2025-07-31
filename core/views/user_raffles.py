# core/views/user_raffles.py
"""
Created on 21 de jul. de 2025

@author: masterdev
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from core.models.raffles import Raffle
from core.models.tickets import Ticket


@login_required
def show_single_raffle(request, raffle_id):
    raffle = get_object_or_404(Raffle, id=raffle_id, status="published")
    # Busca os tickets comprados por este usuário para essa rifa
    user_tickets = Ticket.objects.filter(buyer=request.user, raffle=raffle)

    context = {
        "raffles": [raffle],  # reaproveita o list_raffles.html,
        "user_tickets_map": {
            raffle.id: user_tickets
        },  # usado no template para exibir os tickets
        "single_mode": True,  # opcional, se quiser estilizar diferente
        "available_tickets": _compute_available_tickets(raffle_id),
    }
    return render(request, "core/list_raffles.html", context)


def _compute_available_tickets(raffle_id: int):
    tickets_for_sell = Ticket.objects.filter(
        raffle=raffle_id, buyer__isnull=True
    ).count()
    return tickets_for_sell


@login_required
def list_user_raffles(request):
    print("\nRAFFLES.PY:LIST_USER_RAFFLES\n")
    available_tickets: dict = {}
    user_raffles = Raffle.objects.filter(
        created_by=request.user
    )  # List only the raffles created by logged user
    for raffle in user_raffles:
        # tickets_for_sell = Ticket.objects.filter(
        #     raffle=raffle.id, buyer__isnull=True
        # ).count()
        # tickets_to_sell = raffle.total_tickets - raffle.tickets.filter(payment_confirmed=True).count()
        available_tickets.update(
            {
                "raffles": user_raffles,
                "available_tickets": _compute_available_tickets(raffle.id),
            }
        )
    return render(request, "core/list_raffles.html", available_tickets)
