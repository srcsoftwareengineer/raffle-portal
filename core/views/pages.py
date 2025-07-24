# core/views/pages.py

"""
Created on 23 de jul. de 2025

@author: masterdev
"""
from django.shortcuts import render


def index(request):
    return render(request, "core/index.html")
