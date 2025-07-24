"""
Created on 15 de jul. de 2025

@author: masterdev
"""

import random
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from core.models.raffles import Raffle
from core.models.tickets import Ticket
from core.models.winners import WinnerNotification
from core.app_forms.ticket_form import TicketPurchaseForm
from django.contrib import messages
from core.forms import RaffleForm
from django.urls.base import reverse
from django.utils import timezone
from django.http.response import HttpResponse


def is_superadmin(user):
    return user.is_superuser or user.groups.filter(name="super-admin").exists()


def is_admin(user):
    return user.is_superuser or user.is_staff


@login_required
def dashboard(request):
    return render(request, "core/dashboard.html")


@user_passes_test(is_superadmin, login_url="core:unauthorized")
@login_required
def list_raffles(request):
    available_tickets: dict = {}
    user_raffles = Raffle.objects.all()  # List the raffles created by all users
    for raffle in user_raffles:
        tickets = Ticket.objects.filter(raffle=raffle.id, buyer__isnull=True).count()
        available_tickets.update(
            {"raffles": user_raffles, "available_tickets": tickets}
        )
    return render(request, "core/list_raffles.html", available_tickets)


# @login_required
# def list_raffles(request):
#     print("⚠️ Entrando em list_raffles view!")  # ou use logging
#     raffles = Raffle.objects.all()
#     return render(request, "core/list_raffles.html", {"raffles": raffles})


@login_required
@user_passes_test(is_admin)
def draw_raffle(request, raffle_id):
    raffle = get_object_or_404(Raffle, id=raffle_id)
    tickets = Ticket.objects.filter(
        raffle=raffle, payment_confirmed=True, buyer__isnull=False
    )

    if raffle.drawn_ticket:
        messages.warning(request, "Rifa já sorteada anteriormente.")
        return redirect("core:list_raffles")

    if not tickets.exists():
        messages.error(request, "Não há bilhetes pagos para realizar o sorteio.")
        return redirect("core:list_raffles")

    if raffle.status != "published":
        return redirect("core:list_raffles")

    # Segurança: só o criador da rifa pode sortear
    if raffle.created_by != request.user:
        return redirect("core:list_raffles")

    # Evita múltiplos sorteios
    if raffle.drawn_at is not None:
        return render(
            request,
            "core/draw_winner.html",
            {"raffle": raffle, "winner": raffle.drawn_ticket},
        )

    # Sorteia e salva
    drawn_ticket = random.choice(list(tickets))
    raffle.drawn_at = timezone.now()
    raffle.save()

    # Após sortear o ticket vencedor
    WinnerNotification.objects.update_or_create(
        raffle=raffle, defaults={"drawn_ticket": drawn_ticket, "wapp_sent_by": "User"}
    )
    # Desative a compra de tickets duplicados (opcional)
    # Ticket.objects.filter(raffle=raffle, buyer=raffle.drawn_ticket.buyer).exclude(
    #     id=raffle.drawn_ticket.id
    # ).update(is_reserved=True)

    messages.success(
        request, f"🎉 Ticket {drawn_ticket.number} venceu a rifa '{raffle.title}'!"
    )
    return redirect("core:list_raffles")


@login_required
def draw_winner_display(request, raffle_id):
    raffle = get_object_or_404(Raffle, id=raffle_id)

    try:
        winner_notification = WinnerNotification.objects.get(raffle=raffle)
    except WinnerNotification.DoesNotExist:
        return HttpResponse("Winner not found.", status=404)

    return render(
        request,
        "core/draw_winner_display.html",
        {
            "raffle": raffle,
            "winner_ticket": winner_notification.drawn_ticket,
        },
    )


@login_required
def create_raffle(request):
    if request.method == "POST":
        form = RaffleForm(request.POST)
        if form.is_valid():
            raffle = form.save(commit=False)
            raffle.created_by = request.user
            raffle.save()
            Ticket.objects.bulk_create(
                [
                    Ticket(raffle=raffle, number=i)
                    for i in range(1, raffle.total_tickets + 1)
                ]
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
def purchase_tickets(request, raffle_id):
    raffle = get_object_or_404(Raffle, id=raffle_id)

    if request.method == "POST":
        form = TicketPurchaseForm(request.POST, raffle=raffle)
        if form.is_valid():
            ticket_ids = form.cleaned_data["tickets"]
            selected = Ticket.objects.filter(id__in=ticket_ids, buyer__isnull=True)
            for ticket in selected:
                ticket.buyer = request.user
                ticket.save()
            messages.success(
                request, f"{len(selected)} ticket(s) successfully purchased."
            )
        return redirect(
            reverse("core:purchase_confirmation", kwargs={"raffle_id": raffle.id})
        )
    else:
        form = TicketPurchaseForm(raffle=raffle)
        return render(
            request, "core/purchase_tickets.html", {"raffle": raffle, "form": form}
        )
