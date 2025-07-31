# core/models/raffle_image.py
"""
Created on 24 de jul. de 2025

@author: masterdev
"""

from django.db import models
from core.models.raffles import Raffle


class RaffleImage(models.Model):
    raffle = models.ForeignKey(
        "Raffle", on_delete=models.CASCADE, related_name="images"  # <-- ESSENCIAL
    )
    image = models.ImageField(upload_to="raffle_images/")

    def __str__(self):
        return f"Imagem da Rifa {self.raffle.title}"
