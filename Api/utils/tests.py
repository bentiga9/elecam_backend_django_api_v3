from django.test import TestCase, Client
from django.urls import reverse

class GeneralAPITests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_health_check(self):
        url = reverse('health-check')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})
