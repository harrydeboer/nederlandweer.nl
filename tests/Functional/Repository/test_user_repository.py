from django.contrib.auth.models import User
from django.test import TestCase
from dashboard_meet_je_stad.repository.user_repository import UserRepository
import os
from django.apps import apps


class TestUserRepository(TestCase):
    fixtures = ['fixture.json']

    def setUp(self) -> None:
        self.user_repository = UserRepository()

    def test_get_data(self) -> None:

        user = self.user_repository.find_by_username('test')
        if user is None:
            raise Exception('User not found.')
        self.assertEqual(user.get_username(), 'test')
        user = self.user_repository.find_by_email('test@test.com')
        if user is None:
            raise Exception('User not found.')
        self.assertEqual(user.email, 'test@test.com')

        user = User()
        user.email = 'test22@test22.com'
        user.username = 'test22'
        user = self.user_repository.create(user, 'secret')
        user_id = user.id

        if os.path.isfile(os.path.dirname(apps.get_app_config('dashboard_meet_je_stad').path)
                          + '/tests/data/Stations tbv Mailchimp.xlsx'):
            self.assertEqual(user.dashboarduser.get_sensor_id(), 840)
            self.user_repository.save_dashboard_user(user, 1196)
            user = self.user_repository.get(user_id)
            self.assertEqual(user.dashboarduser.get_sensor_id(), 1196)
            self.user_repository.delete(user)
            self.assertEqual(user.id, None)
