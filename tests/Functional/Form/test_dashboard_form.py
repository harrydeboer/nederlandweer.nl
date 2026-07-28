from django.test import TestCase
from dashboard_meet_je_stad.form.dashboard_form import DashboardForm
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository


class TestDashboardForm(TestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.sensor_repository = SensorRepository()

    def test_forms(self):
        form_data = {'sensor': 1196, 'type': 'temperature', 'interval': '24hour'}
        form = DashboardForm(form_data, sensors=self.sensor_repository.find_all(), inactive=False, pm=False)
        self.assertTrue(form.is_valid())
