"""
Tests for the order app.
"""

from datetime import datetime, timedelta

from rest_framework.test import APITestCase

from interview.inventory.models import (Inventory, InventoryLanguage,
                                        InventoryType)
from interview.order.models import Order


class DeactivateOrderTestCase(APITestCase):
    """
    Integration test for the deactivate order API.
    """
    def setUp(self):
        """Ensures that order ID 1 is active to start with."""
        language = InventoryLanguage.objects.create(name='English')
        inventory_type = InventoryType.objects.create(name='Movie')
        inventory = Inventory.objects.create(
            id=1,
            name='The Lord of the Rings: The Fellowship of the Ring',
            language=language,
            type=inventory_type,
            metadata=dict(
                year=2001,
                actors=['Elijah Wood', 'Ian McKellen', 'Viggo Mortensen'],
                imdb_rating=8.8,
                rotten_toamtoes_rating=91,
            ),
        )
        Order.objects.create(
            id=1,
            inventory=inventory,
            start_date=datetime.now(),
            embargo_date=datetime.now() + timedelta(days=30),
            is_active=True,
        )

    def test_view_deactivates_order(self):
        """Tests that the deactivate view properly deactivates the order."""
        response = self.client.put('/orders/1/deactivate/')
        self.assertEqual(response.status_code, 200)
        order = Order.objects.get(pk=1)
        assert order.is_active == False
