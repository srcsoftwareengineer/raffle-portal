"""
Created on 24 de jul. de 2025

@author: masterdev
"""

from django.shortcuts import render
from core.views import auth


def unauthorized(request):
    return render(request, "core/unauthorized.html")


def campanha_rozini(request):
    return render(request, "campaigns/MVP0.1.0/landingpages/index.html")
