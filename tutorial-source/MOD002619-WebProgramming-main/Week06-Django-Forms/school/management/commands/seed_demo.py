import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import transaction
from school.models import Student, Module

class Command(BaseCommand):
    help = 'Load synthetic student CSV, safely repeatable.'

    @transaction.atomic
    def handle(self, *args, **options):
        for code, name in [('MOD002619', 'Web Programming'), ('MOD003212', 'Introduction to Programming')]:
            Module.objects.get_or_create(code=code, defaults={'name': name})
        with (Path(__file__).resolve().parents[3] / 'data/students.csv').open(encoding='utf-8', newline='') as stream:
            for row in csv.DictReader(stream):
                student, _ = Student.objects.get_or_create(email=row['email'], defaults={'firstName': row['fname'], 'lastName': row['lname'], 'age': row['age']})
                student.modules.set(Module.objects.filter(code__in=row['modules'].split('|')))
        self.stdout.write(self.style.SUCCESS('Synthetic student data ready.'))
