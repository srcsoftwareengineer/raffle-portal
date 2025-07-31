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
from core.models.user_profile import UserProfile
from core.models.raffle_image import RaffleImage
import core.views


def is_superadmin(user):
    return user.is_superuser or user.groups.filter(name="superadmin").exists()


def is_admin(user):
    return user.is_superuser or user.is_staff


@login_required
def dashboard(request):
    return render(request, "core/dashboard.html")


@login_required
def user_home(request):
    print("\nRAFFLES.PY:USER_HOME\n")
    user = request.user
    bought_tickets = Ticket.objects.filter(buyer=user)
    bought_raffles = Raffle.objects.filter(tickets__in=bought_tickets).distinct()
    public_raffles = Raffle.objects.filter(status="published")

    context = {
        "bought_raffles": bought_raffles,
        "public_raffles": public_raffles,
    }
    return render(request, "core/my_raffles.html", context)


@login_required
def my_raffles(request):
    raffles = Raffle.objects.filter(tickets__user=request.user).distinct()
    return render(request, "core/my_raffles.html", {"raffles": raffles})


@user_passes_test(is_superadmin, login_url="core:unauthorized")
@login_required
def list_raffles(request):
    print("\nRAFFLES.PY:LIST_RAFFLES\n")
    available_tickets: dict = {}
    user_raffles = Raffle.objects.all()  # List the raffles created by all users
    for raffle in user_raffles:
        selled_tickets = Ticket.objects.filter(
            raffle=raffle.id, buyer__isnull=True
        ).count()
        # tickets_to_sell = raffle.total_tickets - raffle.tickets.filter(payment_confirmed=True).count()

        available_tickets.update(
            {
                "raffles": user_raffles,
                "available_tickets": selled_tickets,
            }
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

    if not tickets.exists():
        messages.error(request, "Não há bilhetes pagos para realizar o sorteio.")
        return redirect("core:list_user_raffles")

    if raffle.status != "published":
        messages.error(request, "Rifa ainda não foi publicada.")
        return redirect("core:list_user_raffles")

    if raffle.drawn_ticket:
        messages.warning(request, "Rifa já sorteada anteriormente.")
        return redirect("core:list_user_raffles")

    if raffle.status != "published":
        return redirect("core:list_user_raffles")

    # Segurança: só o criador da rifa pode sortear
    if raffle.created_by != request.user:
        return redirect("core:list_user_raffles")

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
            # Imagens
            # image_file = request.FILES.get("images")
            # if image_file:
            #     RaffleImage.objects.create(raffle=raffle, image=image_file)
            for image_file in request.FILES.getlist("images"):
                RaffleImage.objects.create(raffle=raffle, image=image_file)

            Ticket.objects.bulk_create(
                [
                    Ticket(raffle=raffle, number=i)
                    for i in range(1, raffle.total_tickets + 1)
                ]
            )
            return redirect("core:list_user_raffles")
    else:
        form = RaffleForm()
    return render(request, "core/create_raffle.html", {"form": form})


@login_required
def publish_raffle(request, raffle_id):
    raffle = get_object_or_404(Raffle, id=raffle_id, created_by=request.user)
    if raffle.status == "draft":
        raffle.status = "published"
        raffle.save()
    return redirect("core:list_user_raffles")


@login_required
def purchase_tickets(request, raffle_id):
    raffle = get_object_or_404(Raffle, id=raffle_id)

    # ✅ Guard clause: perfil obrigatório
    try:
        profile = request.user.userprofile
        if not profile.ddd or not profile.mobile_number:
            messages.warning(
                request,
                "⚠️ Preencha seu DDD e número de celular antes de participar da rifa.",
            )
            return redirect("core:sign_up")  # ou um "editar perfil", se disponível
    except UserProfile.DoesNotExist:
        messages.warning(request, "⚠️ Complete seu perfil antes de participar da rifa.")
        return redirect("core:sign_up")

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
        available_tickets = form.get_available_tickets(raffle)["available_tickets"]
        return render(
            request,
            "core/purchase_tickets.html",
            {
                "raffle": raffle,
                "form": form,
                "available_tickets": available_tickets,
            },
        )
