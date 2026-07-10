from django.contrib.auth.models import User


class UserRepository:

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