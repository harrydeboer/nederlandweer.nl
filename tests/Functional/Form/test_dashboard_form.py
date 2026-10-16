from django.test import TestCase
from nederland_weer.form.dashboard_form import DashboardForm
from nederland_weer.repository.station_repository import StationRepository


class TestLoginForm(TestCase):
    fixtures = ['fixture.json']

    def test_forms(self):
        stations = StationRepository().find_all()
        form_data = {'station': 260, 'begin_year': 1906, 'end_year': 2025, 'component': 'temperature-day'}
        form = DashboardForm(form_data, stations = stations)
        self.assertTrue(form.is_valid())
