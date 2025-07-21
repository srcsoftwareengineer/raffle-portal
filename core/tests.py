from django.test import TestCase
from django.urls import reverse


class Tests(TestCase):

    def test_dummy_1(self):
        a = 1
        b = 1
        self.assertEquals(a, b)

    def test_purchase_view_accessible(self):
        response = self.client.get(reverse("core:purchase_tickets", args=[1]))
        self.assertIn(response.status_code, [200, 302])
