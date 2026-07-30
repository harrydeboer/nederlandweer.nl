from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils.datastructures import MultiValueDict
from dashboard_meet_je_stad.form.mailchimp_form import MailchimpForm
from django.apps import apps
import os


class TestMailchimpForm(TestCase):
    fixtures = ['fixture.json']

    def test_forms(self):
        file = open(os.path.dirname(apps.get_app_config('dashboard_meet_je_stad').path)
             + '/tests/Stations tbv Mailchimp.xlsx', 'rb+')
        form_data = MultiValueDict()
        form_data['file'] = SimpleUploadedFile("Stations tbv Mailchimp.xlsx", file.read(), content_type="xlsx")
        form = MailchimpForm({}, form_data)
        self.assertTrue(form.is_valid())
