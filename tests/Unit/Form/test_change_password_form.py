from unittest import TestCase
from dashboard_meet_je_stad.form.change_password_form import ChangePasswordForm


class TestChangePasswordForm(TestCase):

    def test_forms(self):
        form_data = {'password': 'secret', 'password_repeat': 'secret'}
        form = ChangePasswordForm(form_data)
        self.assertTrue(form.is_valid())
