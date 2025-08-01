# core/urls.py
"""
Created on 15 de jul. de 2025

@author: masterdev
"""

from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.views import auth, raffles, user_raffles, checkout, pages
from django.conf import settings
from django.conf.urls.static import static

app_name = "core"

urlpatterns = [
    path(
        "accounts/",
        include(("django.contrib.auth.urls", "auth"), namespace="registration"),
    ),
    path("", pages.index, name="index"),  # ⬅️ rota raiz
    # path("dashboard/", raffles.dashboard, name="dashboard"),
    path("dashboard/", raffles.user_home, name="dashboard"),
    # path("dashboard/", raffles.my_raffles, name="dashboard"),
    path(
        "sign-in/",
        auth_views.LoginView.as_view(template_name="registration/sign_in.html"),
        name="sign_in",
    ),
    path("sign-up/", auth.register, name="sign_up"),
    path(
        "logout_view/",
        auth.logout_view,
        name="logout_view",
    ),
    path("raffles/create/", raffles.create_raffle, name="create_raffle"),
    path("raffles/", raffles.list_raffles, name="list_raffles"),
    path("my-raffles/", user_raffles.list_user_raffles, name="list_user_raffles"),
    path(
        "my-raffles/<int:raffle_id>/",
        user_raffles.show_single_raffle,
        name="show_single_raffle",
    ),
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
    path(
        "raffles/draw/<int:raffle_id>/",
        raffles.draw_winner_display,
        name="draw_winner_display",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
