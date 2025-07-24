"""
Created on 15 de jul. de 2025

@author: masterdev
"""

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout


def register(request):
    """
    @todo: Add attributes mobile_prefix and mobile_number

    @note: This the mobile_prefix and the last 4 digits of the mobile number will be
            displayed for public information W.app message will be sent manually
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("core:dashboard")
    else:
        form = UserCreationForm()
    return render(request, "registration/sign_up.html", {"form": form})


def logout_view(request):
    logout(request)
    return render(request, "core/logged_out.html")
