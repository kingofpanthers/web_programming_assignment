from django.test import TestCase
from django.core.management import call_command
from .models import Student

class StudentTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('seed_demo')

    def test_home_detail_and_missing(self):
        self.assertContains(self.client.get('/'), 'Student')
        student = Student.objects.first()
        self.assertContains(self.client.get(f'/student/{student.pk}/'), student.firstName)
        self.assertEqual(self.client.get('/student/999999/').status_code, 404)

    def test_seed_repeatable(self):
        call_command('seed_demo')
        self.assertEqual(Student.objects.count(), 30)

    def test_pagination(self):
        response = self.client.get('/')
        self.assertEqual(len(response.context['page_obj']), 20)
        self.assertEqual(len(self.client.get('/?page=2').context['page_obj']), 10)
        self.assertEqual(self.client.get('/?page=invalid').status_code, 200)
