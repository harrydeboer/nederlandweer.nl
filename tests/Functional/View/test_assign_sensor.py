from django.test import TestCase
from django.test import Client

from dashboard_meet_je_stad.repository.user_repository import UserRepository


class AssignSensorTest(TestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username="superuser", password="secret")
        self.user_repository = UserRepository()

    def test_details(self):
        response = self.client.get("/admin/wijs-sensor-toe")

        self.assertEqual(response.status_code, 200)

        response = self.client.post("/admin/wijs-sensor-toe", {'user': 1, 'sensor': 1})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.user_repository.get(1).dashboarduser.get_sensor_id(), 1)
