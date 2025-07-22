# core/urls.py
"""
Created on 15 de jul. de 2025

@author: masterdev
"""

from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.views import auth, raffles, user_raffles, checkout

app_name = "core"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("", auth.dashboard, name="dashboard"),
    path("dashboard/", auth.dashboard, name="dashboard"),
    path(
        "sign-in/",
        auth_views.LoginView.as_view(template_name="registration/sign_in.html"),
        name="sign_in",
    ),
    path("sign-up/", auth.register, name="sign_up"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="registration/logged_out.html"),
        name="logout",
    ),
    # path("logged_out/", auth.force_logout, name="logged_out"),
    path("raffles/create/", raffles.create_raffle, name="create_raffle"),
    path("raffles/", raffles.list_raffles, name="list_raffles"),
    path("my-raffles/", user_raffles.list_raffles, name="list_raffles"),
    path(
        "raffles/<int:raffle_id>/publish/",
        raffles.publish_raffle,
        name="publish_raffle",
    ),
    path("raffles/<int:raffle_id>/draw/", raffles.draw_raffle, name="draw_raffle"),
    path(
        "raffles/<int:raffle_id>/purchase/",
        raffles.purchase_tickets,
        name="purchase_tickets",
    ),
    path(
        "checkout/purchase_confirmation/<int:raffle_id>/",
        checkout.purchase_confirmation,
        name="purchase_confirmation",
    ),
]
