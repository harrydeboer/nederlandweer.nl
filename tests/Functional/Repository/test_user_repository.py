from django.contrib.auth.models import User
from django.test import TestCase
from nederland_weer.repository.user_repository import UserRepository


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
        self.user_repository.delete(user)
        self.assertEqual(user.id, None)
