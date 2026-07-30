from django.shortcuts import render
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from dashboard_meet_je_stad.form.assign_sensor_form import AssignSensorForm
from dashboard_meet_je_stad.repository.user_repository import UserRepository


class AssignSensorView:

    def __init__(self):
        self.user_repository = UserRepository()

    @method_decorator(staff_member_required)
    def index(self, request: WSGIRequest) -> HttpResponse:
        form = AssignSensorForm(request.POST)

        if form.is_valid():
            user_id = int(form['user'].value())
            user = self.user_repository.get(user_id)
            if form['sensor'].value() != '':
                sensor_id = int(form['sensor'].value())
            else:
                sensor_id = None
            self.user_repository.save_dashboard_user(user, sensor_id)

        dashboard_users = []
        for user in self.user_repository.find_all():
            if hasattr(user, 'dashboarduser'):
                dashboard_users.append(user.dashboarduser)

        return render(request, 'admin/assign_sensor.html',
                      {'form': form, 'dashboard_users': dashboard_users})
