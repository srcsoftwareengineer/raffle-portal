from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect, get_object_or_404
from django.db import transaction
from django.conf import settings
from core.models.winners import WinnerNotification
from core.models.tickets import Ticket
from core.models.raffles import Raffle
from django.contrib.auth.models import User

# from django.contrib.auth import get_user_model
# from django.utils.timezone import now


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

    list_display = (
        "id",
        "title",
        "status_badge",
        "draw_date",
        "ticket_price",
        "total_tickets",
        "tickets_sold",
        "create_date",
        "action_buttons",
        "winner_badge",
    )
    list_filter = ("status", "draw_date", "create_date")
    search_fields = ("title",)
    ordering = ("-create_date",)
    list_editable = (
        "draw_date",
        "ticket_price",
    )
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
    actions = (
        "action_publish",
        "action_unpublish",
        "action_close",
        "action_generate_tickets",
    )

    # --- garante created_by sem default=1 ---
    def save_model(self, request, obj, form, change):
        if not change and not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    # --- colunas auxiliares (como já estavam) ---
    @admin.display(description="Status")
    def status_badge(self, obj):
        color_map = {"draft": "#956106", "published": "#0a7d2c", "closed": "#7d0a0a"}
        return format_html(
            '<span style="padding:2px 8px;border-radius:12px;color:#fff;background:{};">{}</span>',
            color_map.get(obj.status, "#555"),
            obj.get_status_display(),
        )

    @admin.display(description="Tickets vendidos")
    def tickets_sold(self, obj):
        return obj.tickets.filter(payment_confirmed=True).count()

    @admin.display(description="Vencedor")
    def winner_badge(self, obj):
        if obj.drawn_ticket_id:
            t = obj.drawn_ticket
            buyer = t.buyer.username if t.buyer else "—"
            return format_html(
                '<span style="padding:2px 8px;border-radius:12px;background:#1f2937;color:#fff;">#{} · {}</span>',
                t.number,
                buyer,
            )
        return "—"

    @admin.display(description="Ações")
    def action_buttons(self, obj):
        buttons = []
        # Publicar / Encerrar / Sortear (como já estavam)
        if obj.status == "draft":
            buttons.append(
                f'<a class="button" href="./{obj.pk}/publish/" style="margin-right:6px;">Publicar</a>'
            )
        if obj.status == "published":
            buttons.append(
                f'<a class="button" href="./{obj.pk}/close/" style="margin-right:6px;background:#b91c1c;color:white;">Encerrar</a>'
            )
            if obj.tickets.filter(payment_confirmed=True).exists():
                buttons.append(
                    f'<a class="button" href="./{obj.pk}/draw/" style="margin-right:6px;background:#0ea5e9;color:white;">Sortear</a>'
                )
                buttons.append(
                    f'<a class="button" href="./{obj.pk}/close_and_draw/" style="background:#0d9488;color:white;">Encerrar + Sortear</a>'
                )

        # 👉 NOVO: Gerar tickets e Arrematar restantes
        # mostra “Gerar tickets” se faltarem números
        existing = obj.tickets.count()
        if existing < obj.total_tickets:
            buttons.append(
                f'<a class="button" href="./{obj.pk}/generate_tickets/" style="margin-left:6px;background:#4f46e5;color:white;">Gerar tickets</a>'
            )

        # “Arrematar restantes” aparece se houver não pagos
        if obj.tickets.filter(payment_confirmed=False).exists():
            buttons.append(
                f'<a class="button" href="./{obj.pk}/buy_remaining/" style="margin-left:6px;background:#7c3aed;color:white;">Arrematar restantes</a>'
            )

        return format_html("".join(buttons)) if buttons else "—"

    # --- URLs customizadas ---
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
            path(
                "<int:pk>/draw/",
                self.admin_site.admin_view(self.view_draw),
                name="raffle_draw",
            ),
            path(
                "<int:pk>/close_and_draw/",
                self.admin_site.admin_view(self.view_close_and_draw),
                name="raffle_close_draw",
            ),
            # 👉 NOVOS
            path(
                "<int:pk>/generate_tickets/",
                self.admin_site.admin_view(self.view_generate_tickets),
                name="raffle_generate_tickets",
            ),
            path(
                "<int:pk>/buy_remaining/",
                self.admin_site.admin_view(self.view_buy_remaining),
                name="raffle_buy_remaining",
            ),
        ]
        return custom + urls

    # --- Handlers existentes (publish/close/draw/close_and_draw) continuam os teus ---
    # 👉 NOVO: gerar tickets faltantes
    @transaction.atomic
    def view_generate_tickets(self, request, pk):
        raffle = get_object_or_404(Raffle.objects.select_for_update(), pk=pk)
        try:
            before = raffle.tickets.count()
            raffle.generate_missing_tickets()
            created = raffle.tickets.count() - before
            if created > 0:
                self.message_user(
                    request, f"{created} ticket(s) gerado(s).", level=messages.SUCCESS
                )
            else:
                self.message_user(
                    request,
                    "Nenhum ticket novo precisava ser gerado.",
                    level=messages.INFO,
                )
        except Exception as e:
            self.message_user(
                request, f"Erro ao gerar tickets: {e}", level=messages.ERROR
            )
        return redirect(f"../../{pk}/change/")

    # 👉 NOVO: arrematar restantes (firma)
    @transaction.atomic
    def view_buy_remaining(self, request, pk):
        raffle = get_object_or_404(Raffle.objects.select_for_update(), pk=pk)
        try:
            # defina o comprador "firma"
            firm_user_id = getattr(settings, "FIRM_USER_ID", None)
            if not firm_user_id:
                raise ValueError(
                    "Configure settings.FIRM_USER_ID com o ID do usuário 'firma'."
                )
            buyer = get_object_or_404(User, pk=firm_user_id)

            count = raffle.buy_remaining(
                buyer=buyer, confirm_payment=True, reserve=False
            )
            if count:
                self.message_user(
                    request,
                    f"{count} ticket(s) arrematado(s) pela firma.",
                    level=messages.SUCCESS,
                )
            else:
                self.message_user(
                    request,
                    "Não há tickets restantes para arrematar.",
                    level=messages.INFO,
                )
        except Exception as e:
            self.message_user(
                request, f"Erro ao arrematar restantes: {e}", level=messages.ERROR
            )
        return redirect(f"../../{pk}/change/")

    # --- Ações em massa úteis ---
    @admin.action(description="Gerar tickets (faltantes)")
    def action_generate_tickets(self, request, queryset):
        total_created = 0
        for raffle in queryset:
            before = raffle.tickets.count()
            raffle.generate_missing_tickets()
            total_created += raffle.tickets.count() - before
        if total_created:
            self.message_user(
                request,
                f"{total_created} ticket(s) gerado(s) ao todo.",
                level=messages.SUCCESS,
            )
        else:
            self.message_user(
                request, "Nenhum ticket novo precisava ser gerado.", level=messages.INFO
            )


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
