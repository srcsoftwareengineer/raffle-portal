# core/views/checkout.py
"""
Created on 22 de jul. de 2025

@author: masterdev
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def purchase_confirmation(request, raffle_id):
    return render(request, "core/purchase_confirmation.html")
