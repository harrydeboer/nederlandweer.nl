from django.test import TestCase
from dashboard_meet_je_stad.form.assign_sensor_form import AssignSensorForm
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
from dashboard_meet_je_stad.repository.user_repository import UserRepository


class TestAssignSensorForm(TestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.sensor_repository = SensorRepository()
        self.user_repository = UserRepository()

    def test_forms(self):
        form_data = {'user': self.user_repository.get(1).id, 'sensor': self.sensor_repository.get(1196).get_id()}
        form = AssignSensorForm(form_data)
        self.assertTrue(form.is_valid())
