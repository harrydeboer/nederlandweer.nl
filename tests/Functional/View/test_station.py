from django.test import TestCase
from django.test import Client
from nederland_weer.models import Station
from nederland_weer.repository.station_repository import StationRepository


class StationTest(TestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.client = Client()
        self.station_repository = StationRepository()
        self.client.login(username="superuser", password="secret")

    def test_details(self):
        response = self.client.get("/admin/stations")

        self.assertEqual(response.status_code, 200)

        response = self.client.get("/admin/station/nieuw")

        self.assertEqual(response.status_code, 200)

        self.client.post("/admin/station/nieuw",
                         {'id': 1, 'name': 'test',
                          'begin_year': 1906, 'end_year': 2025,
                          'begin_year_perc_rain': 1907, 'begin_year_amount_rain': 1906,
                          'longitude': 3, 'latitude': 3})

        station = self.station_repository.get(1)

        self.assertEqual(station.get_id(), 1)

        response = self.client.get("/admin/station/wijzig/" + str(station.get_id()))

        self.assertEqual(response.status_code, 200)

        self.client.post("/admin/station/wijzig/" + str(station.get_id()),
                         {'id': 1, 'name': 'test2',
                          'begin_year': 1906, 'end_year': 2025,
                          'begin_year_perc_rain': 1907, 'begin_year_amount_rain': 1906,
                          'longitude': 3, 'latitude': 3})

        station = self.station_repository.get(1)

        self.assertEqual(station.get_name(), 'test2')

        self.client.post("/admin/station/verwijder/" + str(station.get_id()))

        test = False
        try:
            self.station_repository.get(1)
        except Station.DoesNotExist:
            test = True

        self.assertTrue(test)
