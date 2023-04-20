"""
Tests for the inventory app.
"""

from datetime import datetime, timedelta

from rest_framework.test import APITestCase

from interview.inventory.models import (Inventory, InventoryLanguage,
                                        InventoryType)


class ListInventoryAfterDateTestCase(APITestCase):
    """
    Integration test to see if orders get filtered appropriately.
    """
    def setUp(self) -> None:
        """Create the test rows."""
        language = InventoryLanguage.objects.create(name='English')
        inventory_type = InventoryType.objects.create(name='Movie')
        Inventory.objects.create(
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
        Inventory.objects.filter(pk=1).update(created_at=datetime.now() - timedelta(days=30))
        Inventory.objects.create(
            id=2,
            name='The Lord of the Rings: The Return of the King',
            language=language,
            type=inventory_type,
            metadata=dict(
                year=2003,
                actors=['Elijah Wood', 'Ian McKellen', 'Viggo Mortensen'],
                imdb_rating=8.9,
                rotten_tomatoes_rating=95,
            ),
        )
        Inventory.objects.filter(pk=2).update(created_at=datetime.now() + timedelta(days=30))

    def test_inventory_after_view_filters(self):
        """We should get inventory item 2 but not 1."""
        today = datetime.now()
        response = self.client.get(f'/inventory/{today.year}/{today.month}/{today.day}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
