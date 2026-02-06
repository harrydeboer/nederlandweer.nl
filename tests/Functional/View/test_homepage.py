from django.test import TestCase
from django.test import Client
from nederland_weer.repository.station_repository import StationRepository


class HomepageTest(TestCase):
    def setUp(self):
        StationRepository().create({'id': 260, 'name': "De Bilt", 'begin_year': 1906, 'end_year': 2025,
                                    'begin_year_perc_rain': 1930, 'begin_year_amount_rain': 1906})
        self.client = Client()

    def test_details(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            "/?station=260&begin_year=1906&end_year=2025&component=temperature-day",
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content.decode("utf-8").find('zomerdag'), -1)

        response = self.client.get(
            "/?station=260&begin_year=1906&end_year=2025&component=temperature-year",
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content.decode("utf-8").find('Temperatuur stijging'), -1)

        response = self.client.get(
            "/?station=260&begin_year=1906&end_year=2025&component=amount-rain",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            "/?station=260&begin_year=1930&end_year=2025&component=perc-rain",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            "/?station=260&begin_year=1906&end_year=2025&component=perc-sunshine",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            "/?station=260&begin_year=1906&end_year=2025&component=wind-speed",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            "/?station=260&begin_year=1906&end_year=2025&component=wind-speed-va",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            "/?station=260&begin_year=1906&end_year=2025&component=tropical",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            "/?station=260&begin_year=1906&end_year=2025&component=extreme",
        )
        self.assertEqual(response.status_code, 200)
