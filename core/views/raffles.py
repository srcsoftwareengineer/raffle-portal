"""
Created on 15 de jul. de 2025

@author: masterdev
"""

import random
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models.raffles import Raffle
from core.models.tickets import Ticket
from core.models.winners import WinnerNotification
from core.forms import RaffleForm


@login_required
def draw_raffle(request, raffle_id):
    raffle = get_object_or_404(
        Raffle, id=raffle_id, created_by=request.user, status="published"
    )
    tickets = Ticket.objects.filter(raffle=raffle, payment_confirmed=True)

    if tickets.exists():
        winner_ticket = random.choice(tickets)
        WinnerNotification.objects.create(raffle=raffle, winner=winner_ticket.buyer)
        raffle.status = "finished"
        raffle.save()
    return redirect("core:list_raffles")


@login_required
def create_raffle(request):
    if request.method == "POST":
        form = RaffleForm(request.POST)
        if form.is_valid():
            raffle = form.save(commit=False)
            raffle.created_by = request.user
            raffle.save()
            for i in range(1, raffle.total_tickets + 1):
                Ticket.objects.create(
                    raffle=raffle, number=i, ticket_price=raffle.ticket_price
                )
            return redirect("core:list_raffles")
    else:
        form = RaffleForm()
    return render(request, "core/create_raffle.html", {"form": form})


@login_required
def publish_raffle(request, raffle_id):
    raffle = get_object_or_404(Raffle, id=raffle_id, created_by=request.user)
    if raffle.status == "draft":
        raffle.status = "published"
        raffle.save()
    return redirect("core:list_raffles")


@login_required
def list_raffles(request):
    raffles = Raffle.objects.filter(created_by=request.user)
    return render(request, "core/list_raffles.html", {"raffles": raffles})
