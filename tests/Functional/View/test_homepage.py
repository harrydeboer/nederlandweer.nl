from django.test import TestCase
from django.test import Client


class HomepageTest(TestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.client = Client()

    def test_details(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            "/?station=260&begin_year=01-01-1901&end_year=01-01-2026&component=temperature-day",
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content.decode("utf-8").find('zomerdag'), -1)

        response = self.client.get(
            "/?station=260&begin_year=01-01-1901&end_year=01-01-2026&component=temperature-year",
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content.decode("utf-8").find('Temperatuur stijging'), -1)

        response = self.client.get(
            "/?station=260&begin_year=01-01-1901&end_year=01-01-2026&component=amount-rain",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            "/?station=260&begin_year=01-01-1930&end_year=01-01-2026&component=perc-rain",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            "/?station=260&begin_year=01-01-1901&end_year=01-01-2026&component=perc-sunshine",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            "/?station=260&begin_year=01-01-1901&end_year=01-01-2026&component=wind-speed",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            "/?station=260&begin_year=01-01-1901&end_year=01-01-2026&component=wind-speed-va",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            "/?station=260&begin_year=01-01-1901&end_year=01-01-1901&component=tropical",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            "/?station=260&begin_year=01-01-1901&end_year=01-01-2026&component=extreme",
        )
        self.assertEqual(response.status_code, 200)
