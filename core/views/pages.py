# core/views/pages.py

"""
Created on 23 de jul. de 2025

@author: masterdev
"""
from django.shortcuts import render
from core.models import Raffle, Ticket
from django.db.models import Q

# def index(request):
#     return render(request, "core/index.html")


def index(request):
    published_raffles = Raffle.objects.filter(status="published").order_by(
        "-create_date"
    )[:6]
    return render(request, "core/index.html", {"raffles": published_raffles})


def home_page(request):
    if request.user.is_authenticated:
        purchased = Raffle.objects.filter(tickets__user=request.user).distinct()
        available = (
            Raffle.objects.filter(published=True)
            .exclude(Q(tickets__user=request.user))
            .distinct()
        )
        context = {"purchased_raffles": purchased, "available_raffles": available}
    else:
        context = {"raffles": Raffle.objects.filter(published=True)}

    return render(request, "core/list_raffles.html", context)
