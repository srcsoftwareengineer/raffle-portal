from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from core.models.raffles import Raffle
from core.models.tickets import Ticket


class DrawWinnerTest(TestCase):

    def test_draw_selects_a_ticket(self):
        user = User.objects.create_user(username="admin", password="123")
        raffle = Raffle.objects.create(
            title="Test", created_by=user, status="published", total_tickets=1
        )
        ticket = Ticket.objects.create(
            raffle=raffle, number=1, buyer=user, payment_confirmed=True
        )

        self.client.force_login(user)
        response = self.client.get(reverse("core:draw_raffle", args=[raffle.id]))
        self.assertContains(response, "Winner Ticket")


class Tests(TestCase):

    def test_dummy_1(self):
        a = 1
        b = 1
        self.assertEquals(a, b)

    def test_purchase_view_accessible(self):
        response = self.client.get(reverse("core:purchase_tickets", args=[1]))
        self.assertIn(response.status_code, [200, 302])
