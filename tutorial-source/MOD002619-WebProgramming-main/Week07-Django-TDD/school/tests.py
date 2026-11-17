import hashlib
from django.test import TestCase, Client
from .models import Hash
from .forms import HashForm
from .views import digest
HELLO = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'

class HashTests(TestCase):

    def test_form_validation(self):
        self.assertTrue(HashForm({'text': 'hello'}).is_valid())
        self.assertFalse(HashForm({'text': ''}).is_valid())
        self.assertFalse(HashForm({'text': 'x' * 10001}).is_valid())

    def test_digest_known_and_unicode(self):
        self.assertEqual(digest('hello'), HELLO)
        self.assertEqual(digest(' café '), hashlib.sha256(' café '.encode()).hexdigest())

    def test_save_redirect_retrieve_and_deduplicate(self):
        for _ in range(2):
            response = self.client.post('/', {'text': 'hello'}, follow=True)
            self.assertContains(response, HELLO)
        self.assertEqual(Hash.objects.count(), 1)
        self.assertEqual(Hash.objects.get(hash=HELLO).text, 'hello')

    def test_invalid_form_and_unknown_hash(self):
        self.assertEqual(self.client.get('/hash/missing/').status_code, 404)
        self.client.post('/', {'text': ''})
        self.assertEqual(Hash.objects.count(), 0)

    def test_ajax_preview_does_not_save(self):
        self.assertEqual(self.client.post('/quickhash/', {'text': 'hello'}).json()['hash'], HELLO)
        self.assertEqual(Hash.objects.count(), 0)
        self.assertEqual(self.client.post('/quickhash/', {'text': 'x' * 10001}).status_code, 400)

    def test_csrf_required(self):
        self.assertEqual(Client(enforce_csrf_checks=True).post('/quickhash/', {'text': 'hello'}).status_code, 403)
