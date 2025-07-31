"""
Created on 15 de jul. de 2025

@author: Sandro Regis Cardoso
"""

from django import forms
from core.models.raffles import Raffle
from django.contrib.auth.models import User
from core.models.user_profile import UserProfile
from django.forms.widgets import FileInput

ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]
MAX_IMAGES = 4  # Defina o limite máximo de arquivos


class UserRegistrationForm(forms.ModelForm):
    """
    @note: This the mobile_prefix and the last 4 digits of the mobile number will be
            displayed for public information W.app message will be sent manually
    """

    password = forms.CharField(widget=forms.PasswordInput)
    ddd = forms.CharField(label="DDD", max_length=2)
    mobile_number = forms.CharField(label="Celular", max_length=15)

    class Meta:
        model = User
        # fields = ["username", "email", "password", "first_name", "last_name"]
        fields = ["username", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        ddd = cleaned_data.get("ddd")
        mobile_number = cleaned_data.get("mobile_number")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")

        if UserProfile.objects.filter(ddd=ddd, mobile_number=mobile_number).exists():
            raise forms.ValidationError("Este número de telefone já está cadastrado.")

        return cleaned_data


# class CustomSignUpForm(UserCreationForm):
# mobile_prefix = forms.CharField(...)
# mobile_number = forms.CharField(...)

# def clean(self):
# cleaned_data = super().clean()
# mobile_prefix = cleaned_data.get("mobile_prefix")
# mobile_number = cleaned_data.get("mobile_number")

# if UserProfile.objects.filter(mobile_prefix=mobile_prefix, mobile_number=mobile_number).exists():
# raise ValidationError("Este número de telefone já está cadastrado em outra conta.")

# return cleaned_data


class RaffleForm(forms.ModelForm):
    images = forms.FileField(
        widget=FileInput(attrs={"multiple": False}),
        required=False,
        label="Imagens da Rifa",
    )

    class Meta:
        model = Raffle
        fields = [
            "title",
            "description",
            "draw_date",
            "ticket_price",
            "total_tickets",
            "status",
        ]
        widgets = {
            "draw_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_images(self):
        image_file = self.files.get("images")

        if not image_file:
            return None

        ext = image_file.name.split(".")[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise forms.ValidationError(
                f"Tipo de arquivo não suportado: {ext}. Permitidos: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        if image_file.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Imagem muito grande (máx. 5MB)")

        return image_file


class PurchaseTicketForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label="Quantidade de Tickets")
