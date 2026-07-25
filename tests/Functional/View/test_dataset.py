from django.test import TestCase
from django.test import Client
from django.http import HttpResponse, FileResponse


class HomepageTest(TestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username="superuser", password="secret")

    def test_details(self):
        response = self.client.get("/dataset")

        self.assertEqual(response.status_code, 200)

        response = self.client.get("/dataset?start=3&end=&ids=&cutoff_temp=on&cutoff_temp_min=-25&cutoff_temp_max=70" +
                                   "&cutoff_pm25=on&cutoff_pm25_min=0&cutoff_pm25_max=250&cutoff_pm10=on" +
                                   "&cutoff_pm10_min=0&cutoff_pm10_max=250")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response, HttpResponse))

        response = self.client.get("/dataset?start=2026-01-01,00:00:00&end=2026-01-02,00:00:00&ids=&cutoff_temp=on" +
                                   "&cutoff_temp_min=-25&cutoff_temp_max=70" +
                                   "&cutoff_pm25=on&cutoff_pm25_min=0&cutoff_pm25_max=250&cutoff_pm10=on" +
                                   "&cutoff_pm10_min=0&cutoff_pm10_max=250")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response, FileResponse))

        response = self.client.get("/dataset?start=2026-01-01,00:00:00&end=2026-01-02,00:00:00&ids=1-5&cutoff_temp=on" +
                                   "&cutoff_temp_min=-25&cutoff_temp_max=70" +
                                   "&cutoff_pm25=on&cutoff_pm25_min=0&cutoff_pm25_max=250&cutoff_pm10=on" +
                                   "&cutoff_pm10_min=0&cutoff_pm10_max=250")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response, FileResponse))
