from django.test import TestCase
from django.test import Client


class SitemapTest(TestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.client = Client()

    def test_details(self):
        response = self.client.get("/sitemap.xml")

        self.assertEqual(response.status_code, 200)
