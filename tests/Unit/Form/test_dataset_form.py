from unittest import TestCase
from dashboard_meet_je_stad.form.dataset_form import DatasetForm


class TestDatasetForm(TestCase):

    def test_forms(self):
        form_data = {'start': '2026-01-01,00:00:00', 'end': '2026-01-02,00:00:00'}
        form = DatasetForm(form_data)
        self.assertTrue(form.is_valid())
