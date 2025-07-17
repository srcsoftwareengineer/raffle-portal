from django.test import TestCase


class Tests(TestCase):
    def test_dummy(self):
        a = 1
        b = 1
        self.assertEqual(a, b)
