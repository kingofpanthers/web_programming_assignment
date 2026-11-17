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

    def test_filter_and_empty_result(self):
        response = self.client.get('/?firstName=a')
        self.assertEqual(response.context['page_obj'].paginator.count, 25)
        self.assertContains(response, 'firstName=a')
        response = self.client.get('/?firstName=a&page=2')
        self.assertEqual(len(response.context['page_obj']), 5)
        self.assertContains(self.client.get('/?firstName=NoSuchName'), 'No records returned')

    def test_edit_and_invalid_submission(self):
        student = Student.objects.first()
        data = {'firstName': 'Updated', 'lastName': 'Name', 'age': 25, 'email': 'valid@example.com', 'enrolmentDate': '2026-01-01T12:00'}
        response = self.client.post(f'/student/{student.pk}/edit/', data)
        self.assertEqual(response.status_code, 302)
        student.refresh_from_db()
        self.assertEqual(student.firstName, 'Updated')
        data['age'] = -1
        response = self.client.post(f'/student/{student.pk}/edit/', data)
        self.assertTrue(response.context['form'].errors)
        student.refresh_from_db()
        self.assertEqual(student.age, 25)

    def test_image_upload(self):
        import io, tempfile
        from PIL import Image
        from django.core.files.uploadedfile import SimpleUploadedFile
        student = Student.objects.first()
        image = io.BytesIO()
        Image.new('RGB', (2, 2)).save(image, format='PNG')
        data = {'firstName': 'Portrait', 'lastName': 'Test', 'age': 20, 'email': 'portrait@example.com', 'enrolmentDate': '2026-01-01T12:00', 'image': SimpleUploadedFile('portrait.png', image.getvalue(), content_type='image/png')}
        with tempfile.TemporaryDirectory() as directory, self.settings(MEDIA_ROOT=directory):
            self.assertEqual(self.client.post(f'/student/{student.pk}/edit/', data).status_code, 302)
            student.refresh_from_db()
            self.assertTrue(student.image.name.endswith('.png'))
