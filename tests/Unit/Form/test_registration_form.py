from unittest import TestCase
from dashboard_meet_je_stad.form.registration_form import RegistrationForm


class TestRegistrationForm(TestCase):

    def test_forms(self):
        form_data = {'username': 'test', 'email': 'test@test.com', 'password': 'secret', 'password_repeat': 'secret'}
        form = RegistrationForm(form_data)
        self.assertTrue(form.is_valid())
