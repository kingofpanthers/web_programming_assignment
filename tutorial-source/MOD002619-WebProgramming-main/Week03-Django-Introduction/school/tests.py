from django.test import TestCase
from django.core.management import call_command
from .models import Player, Position

class RugbyTests(TestCase):

    def test_csv_repeatable_and_relationships(self):
        call_command('seed_demo')
        call_command('seed_demo')
        self.assertEqual(Player.objects.count(), 3)
        self.assertEqual(Position.objects.filter(specialist=True).count(), 4)
        self.assertEqual(Player.objects.get(name='Alex Morgan').positions.count(), 2)
        self.assertContains(self.client.get('/'), 'Alex Morgan')
