from django.contrib.auth.models import User
from typing import List

from dashboard_meet_je_stad.models import DashboardUser


class UserRepository:

    def get(self, user_id: int) -> User:

        return User.objects.get(pk=user_id)

    def find_all(self) -> List[User]:
        return list(User.objects.all())

    def find_by_username(self, username: str) -> User | None:
        return User.objects.filter(username=username).first()

    def find_by_email(self, email: str) -> User | None:
        return User.objects.filter(email=email).first()

    def create(self, user: User, password: str) -> User:
        user.set_password(password)
        user.save()
        return user

    def update(self, user: User, password: str | None = None) -> User:
        if password is not None:
            user.set_password(password)
        user.save()
        return user

    def delete(self, user: User) -> None:
        user.delete()

    def save_dashboard_user(self, user: User, sensor_id: int):
        dashboard_user = DashboardUser.objects.filter(_user=user, _sensor_id=sensor_id).first()
        if dashboard_user is not None:
            dashboard_user.set_sensor_id(sensor_id)
            dashboard_user.save()
        else:
            dashboard_user = DashboardUser()
            dashboard_user.set_sensor_id(sensor_id)
            dashboard_user.set_user(user)
            dashboard_user.save()
