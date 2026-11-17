import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import transaction
from school.models import Player, Position

class Command(BaseCommand):
    help = 'Import the included sample rugby CSV; safe to run again.'

    @transaction.atomic
    def handle(self, *args, **options):
        names = ['Tight Head Prop', 'Hooker', 'Loose Head Prop', 'Second Row', 'Open Side Flanker', 'Blind Side Flanker', 'Number 8', 'Scrum Half', 'Fly Half', 'Inside Centre', 'Outside Centre', 'Left Wing', 'Right Wing', 'Full Back']
        # The first four positions in the worksheet are specialist roles.
        for i, name in enumerate(names):
            Position.objects.get_or_create(name=name, defaults={'specialist': i < 4})
        with (Path(__file__).resolve().parents[3] / 'data/players.csv').open(encoding='utf-8', newline='') as stream:
            for row in csv.DictReader(stream):
                player, _ = Player.objects.get_or_create(name=row['name'], team=row['team'])
                player.positions.set([Position.objects.get(name=p.strip()) for p in row['positions'].split('|')])
        self.stdout.write(self.style.SUCCESS('Rugby sample data ready.'))
