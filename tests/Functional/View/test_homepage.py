from django.test import TestCase
from django.test import Client


class HomepageTest(TestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username="superuser", password="secret")

    def test_details(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            "/?sensor=1196&type=temperature&interval=24hour",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/?sensor=&type=temperature&interval=24hour&inactive=on")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("?sensor=1196&type=temperature&interval=3month")
        self.assertEqual(response.status_code, 200)
