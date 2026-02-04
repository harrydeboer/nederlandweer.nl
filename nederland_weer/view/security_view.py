from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from nederland_weer.form.login_form import LoginForm
from nederland_weer.form.registration_form import RegistrationForm
from django.contrib.auth.models import User


class SecurityView:

    def login(self, request: WSGIRequest) -> HttpResponse:
        form = LoginForm(request.POST)
        if form.is_valid():

            user = authenticate(username=form['username'].value(), password=form['password'].value())
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error('password', 'Ongeldige inlog.')
        else:
            user = request.user

        return render(request, 'security/login.html', {'form': form, 'user': user})

    def registrate(self, request: WSGIRequest) -> HttpResponse:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if form['password'].value() == form['password_repeat'].value():
                user = User.objects.create_user(form['username'].value(),
                                                form['email'].value(),
                                                form['password'].value())
                user.save()
            else:
                form.add_error('password', 'Wachtwoorden zijn niet hetzelfde.')

        return render(request, 'security/registration.html', {'form': form})

    def logout(self, request: WSGIRequest) -> HttpResponse:
        logout(request)

        return redirect('home')
