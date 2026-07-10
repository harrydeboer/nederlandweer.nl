from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from dashboard_meet_je_stad.form.change_password_form import ChangePasswordForm
from dashboard_meet_je_stad.form.login_form import LoginForm
from dashboard_meet_je_stad.form.registration_form import RegistrationForm
from dashboard_meet_je_stad.repository.user_repository import UserRepository
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class SecurityView:

    def __init__(self):
        self.user_repository = UserRepository()

    def login(self, request: WSGIRequest) -> HttpResponse:
        form = LoginForm(request.POST)
        if form.is_valid():

            user = authenticate(username=form['username'].value(), password=form['password'].value())
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error('password', 'Ongeldige inlog.')
                user = request.user
        else:
            user = request.user

        return render(request, 'security/login.html', {'form': form, 'user': user})

    def registrate(self, request: WSGIRequest) -> HttpResponse:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if form['password'].value() == form['password_repeat'].value():
                user = User()
                user.username = form['username'].value()
                user.email = form['email'].value()
                user.password = form['password'].value()
                if self.user_repository.find_by_username(user.username):
                    form.add_error('username', 'Gebruikersnaam bestaat al.')
                if self.user_repository.find_by_email(user.email):
                    form.add_error('email', 'Email bestaat al.')
                if not form.errors:
                    self.user_repository.create(user, form['password'].value())
                    login(request, user)
                    return redirect('home')
            else:
                form.add_error('password', 'Wachtwoorden zijn niet hetzelfde.')

        return render(request, 'security/registration.html', {'form': form})

    @method_decorator(login_required, name='dispatch')
    def change_password(self, request: WSGIRequest) -> HttpResponse:
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            if form['password'].value() == form['password_repeat'].value():
                user = request.user
                if isinstance(user, User):
                    self.user_repository.update(user, form['password'].value())
                    login(request, user)
                return redirect('home')
            else:
                form.add_error('password', 'Wachtwoorden zijn niet hetzelfde.')
        return render(request, 'security/change_password.html', {'form': form})

    def logout(self, request: WSGIRequest) -> HttpResponse:
        logout(request)

        return redirect('home')
