from django.test import TestCase
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.apps import apps


class MailchimpTest(TestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username="superuser", password="secret")

    def test_details(self):
        response = self.client.get("/admin/mailchimp")

        self.assertEqual(response.status_code, 200)

        file = open(os.path.dirname(apps.get_app_config('dashboard_meet_je_stad').path)
                    + '/tests/Stations tbv Mailchimp.xlsx', 'rb+')

        self.client.post("/admin/mailchimp", {'file':
                                                  SimpleUploadedFile("Stations tbv Mailchimp.xlsx",
                                                                     file.read(), content_type="xlsx")})
