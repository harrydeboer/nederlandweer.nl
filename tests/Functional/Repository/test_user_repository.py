from django.test import TestCase
from dashboard_meet_je_stad.repository.user_repository import UserRepository


class TestUserRepository(TestCase):
    fixtures = ['fixture.json']

    def test_get_data(self) -> None:
        repository = UserRepository()

        result = repository.find_by_username('test')
        self.assertIsNotNone(result)
