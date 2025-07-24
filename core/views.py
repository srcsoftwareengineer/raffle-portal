"""
Created on 24 de jul. de 2025

@author: masterdev
"""

from django.shortcuts import render


def unauthorized(request):
    return render(request, "core/unauthorized.html")
