"""
Created on 15 de jul. de 2025

@author: masterdev
"""

from django.shortcuts import render, reverse
from django.shortcuts import redirect
from django.contrib.auth import logout
from core.forms import UserRegistrationForm
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = "registration/login.html"

    def get_success_url(self):
        return self.get_redirect_url() or reverse("core:user_home")


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Salva info temporária da sessão para ser usada em algum momento
            request.session["ddd"] = form.cleaned_data["ddd"]
            request.session["mobile_number"] = form.cleaned_data["mobile_number"]
            # Atualiza o perfil com DDD e celular
            profile = user.userprofile
            profile.ddd = form.cleaned_data["ddd"]
            profile.mobile_number = form.cleaned_data["mobile_number"]
            profile.save()
            next_url = request.GET.get("next", "")
            login_url = reverse("core:sign_in")
            if next_url:
                login_url += f"?next={next_url}"
            return redirect(login_url)
            # return redirect("core:sign_in")
    else:
        form = UserRegistrationForm()
    return render(request, "core/sign_up.html", {"form": form})


def logout_view(request):
    username = request.user.username
    logout(request)
    request.session["just_logged_out_user"] = username
    return render(request, "core/logged_out.html", {"username": username})


def logged_out(request):
    username = request.session.pop("just_logged_out_user", "convidado")
    return render(request, "core/logged_out.html", {"username": username})
