from django.test import TestCase
from nederland_weer.form.station_form import StationForm
from nederland_weer.repository.station_repository import StationRepository


class TestLoginForm(TestCase):
    fixtures = ['fixture.json']

    def test_forms(self):
        stations = StationRepository().find_all()
        form_data = {'id': 260, 'name': 'De Bilt', 'longitude': 1, 'latitude': 1}
        form = StationForm(form_data, station=stations['De Bilt'])
        self.assertTrue(form.is_valid())
