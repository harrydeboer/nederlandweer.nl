from django.test import TestCase
from django.test import Client


class HomepageTest(TestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username="superuser", password="secret")

    def test_details(self):
        response = self.client.get("/dataset")

        self.assertEqual(response.status_code, 200)
