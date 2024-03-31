from decimal import Decimal

from django.test import TestCase


class ApproximatelyEqualMixin(TestCase):
    def assert_approximately_equal(self, response, expected):
        self.assertAlmostEqual(Decimal(response), Decimal(expected), places=5)
