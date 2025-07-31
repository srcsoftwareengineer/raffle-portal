from django.contrib import admin
from core.models.winners import WinnerNotification
from core.models.tickets import Ticket
from core.models.raffles import Raffle
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect, get_object_or_404
from django.utils.timezone import now
from django.db import transaction


# -----------------------------
# Inline de Tickets
# -----------------------------
class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0
    fields = ("number", "buyer", "is_reserved", "payment_confirmed")
    readonly_fields = ("number",)
    can_delete = False


# -----------------------------
# Admin de Raffle
# -----------------------------
@admin.register(Raffle)
class RaffleAdmin(admin.ModelAdmin):
    save_on_top = True
    list_per_page = 25

    # Listagem principal
    list_display = (
        "id",
        "title",
        "status_badge",
        "draw_date",
        "ticket_price",
        "total_tickets",
        "tickets_sold",
        "create_date",
        "publish_button",
    )
    list_filter = ("status", "draw_date", "create_date")
    search_fields = ("title",)
    ordering = ("-create_date",)

    # Permitir edição rápida de alguns campos direto da listagem
    list_editable = (
        "draw_date",
        "ticket_price",
    )

    # Fieldsets
    fieldsets = (
        ("Dados gerais", {"fields": ("title", "description", "status")}),
        (
            "Configuração da Rifa",
            {"fields": ("draw_date", "ticket_price", "total_tickets")},
        ),
        (
            "Sistema",
            {
                "classes": ("collapse",),
                "fields": ("create_date", "drawn_at", "created_by", "drawn_ticket"),
            },
        ),
    )

    readonly_fields = ("create_date", "drawn_at", "created_by", "drawn_ticket")

    inlines = [TicketInline]

    # Ações em massa
    actions = ("action_publish", "action_unpublish", "action_close")

    # Badge de status colorida
    @admin.display(description="Status")
    def status_badge(self, obj):
        color_map = {
            "draft": "#956106",  # âmbar
            "published": "#0a7d2c",  # verde
            "closed": "#7d0a0a",  # vermelho
        }
        return format_html(
            '<span style="padding:2px 8px; border-radius:12px; color:#fff; background:{};">{}</span>',
            color_map.get(obj.status, "#555"),
            obj.get_status_display(),
        )

    # Contador de tickets vendidos
    @admin.display(description="Tickets vendidos")
    def tickets_sold(self, obj):
        return obj.tickets.filter(payment_confirmed=True).count()

    # Botão de publicar na listagem
    @admin.display(description="Publicar")
    def publish_button(self, obj):
        if obj.status == "draft":
            return format_html(
                '<a class="button" href="{}">Publicar</a>', f"./{obj.pk}/publish/"
            )
        return "—"

    # Custom URLs (para botão "Publicar")
    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "<int:pk>/publish/",
                self.admin_site.admin_view(self.view_publish),
                name="raffle_publish",
            ),
        ]
        return custom + urls

    @transaction.atomic
    def view_publish(self, request, pk):
        raffle = get_object_or_404(Raffle, pk=pk)
        try:
            if raffle.total_tickets <= 0:
                raise ValueError("Defina um número de bilhetes maior que zero.")
            raffle.status = "published"
            raffle.drawn_at = None
            raffle.save()
            self.message_user(
                request, "Rifa publicada com sucesso!", level=messages.SUCCESS
            )
        except Exception as e:
            self.message_user(request, f"Erro ao publicar: {e}", level=messages.ERROR)
        return redirect(f"../../{pk}/change/")

    # Ações em massa
    @admin.action(description="Publicar rifas selecionadas")
    def action_publish(self, request, queryset):
        queryset.update(status="published")
        self.message_user(
            request, "Rifas publicadas com sucesso.", level=messages.SUCCESS
        )

    @admin.action(description="Mover rifas selecionadas para rascunho")
    def action_unpublish(self, request, queryset):
        queryset.update(status="draft")
        self.message_user(
            request, "Rifas movidas para rascunho.", level=messages.SUCCESS
        )

    @admin.action(description="Encerrar rifas selecionadas")
    def action_close(self, request, queryset):
        queryset.update(status="closed")
        self.message_user(request, "Rifas encerradas.", level=messages.SUCCESS)

    # ... resto do código permanece igual ...

    # Botão de publicar / encerrar na listagem
    @admin.display(description="Ações")
    def publish_button(self, obj):
        if obj.status == "draft":
            return format_html(
                '<a class="button" href="{}" style="margin-right:5px;">Publicar</a>',
                f"./{obj.pk}/publish/",
            )
        elif obj.status == "published":
            return format_html(
                '<a class="button" style="background:#b91c1c;color:white;" href="{}">Encerrar vendas</a>',
                f"./{obj.pk}/close/",
            )
        return "—"

    # URLs customizadas (adiciona rota /publish/ e /close/)
    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "<int:pk>/publish/",
                self.admin_site.admin_view(self.view_publish),
                name="raffle_publish",
            ),
            path(
                "<int:pk>/close/",
                self.admin_site.admin_view(self.view_close),
                name="raffle_close",
            ),
        ]
        return custom + urls

    @transaction.atomic
    def view_publish(self, request, pk):
        raffle = get_object_or_404(Raffle, pk=pk)
        try:
            if raffle.total_tickets <= 0:
                raise ValueError("Defina um número de bilhetes maior que zero.")
            raffle.status = "published"
            raffle.drawn_at = None
            raffle.save()
            self.message_user(
                request, "Rifa publicada com sucesso!", level=messages.SUCCESS
            )
        except Exception as e:
            self.message_user(request, f"Erro ao publicar: {e}", level=messages.ERROR)
        return redirect(f"../../{pk}/change/")

    @transaction.atomic
    def view_close(self, request, pk):
        raffle = get_object_or_404(Raffle, pk=pk)
        try:
            if raffle.status != "published":
                raise ValueError("Apenas rifas publicadas podem ser encerradas.")
            raffle.status = "closed"
            raffle.save()
            self.message_user(
                request, "Rifa encerrada com sucesso!", level=messages.SUCCESS
            )
        except Exception as e:
            self.message_user(request, f"Erro ao encerrar: {e}", level=messages.ERROR)
        return redirect(f"../../{pk}/change/")


# -----------------------------
# Admin de Tickets
# -----------------------------
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "raffle",
        "number",
        "buyer",
        "is_reserved",
        "payment_confirmed",
    )
    list_filter = ("payment_confirmed", "is_reserved", "raffle")
    search_fields = ("buyer__username", "number")
    ordering = ("raffle", "number")
    list_editable = ("payment_confirmed", "is_reserved")


# @admin.register(Ticket)
# class TicketAdmin(admin.ModelAdmin):
#     list_display = ("id", "raffle", "number", "buyer", "payment_confirmed")
#     list_filter = ("raffle", "payment_confirmed")
#     search_fields = ("number", "buyer__username")
#     list_editable = ("payment_confirmed",)


@admin.register(WinnerNotification)
class WinnerNotificationAdmin(admin.ModelAdmin):
    list_display = ("raffle", "winner", "wapp_sent")
    list_filter = ("wapp_sent",)


# DEVTOOLS
# from django.contrib.auth.models import Group, User
#
# group, created = Group.objects.get_or_create(name="super-admin")
# admin_user = User.objects.get(username="admin")
# admin_user.groups.add(group)
