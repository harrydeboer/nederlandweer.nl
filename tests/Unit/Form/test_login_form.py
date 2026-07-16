from unittest import TestCase
from dashboard_meet_je_stad.form.login_form import LoginForm


class TestLoginForm(TestCase):

    def test_forms(self):
        form_data = {'username': 'test', 'password': 'secret'}
        form = LoginForm(form_data)
        self.assertTrue(form.is_valid())
