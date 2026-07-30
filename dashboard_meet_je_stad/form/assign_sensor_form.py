from django import forms
from django.forms.fields import ChoiceField
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
from dashboard_meet_je_stad.repository.user_repository import UserRepository


class AssignSensorForm(forms.Form):

    def __init__(self, *args, **kwargs):
        if len(args[0]) > 0:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(**kwargs)
        sensor_repository= SensorRepository()
        user_repository= UserRepository()
        choices = [("", "-")]
        users = user_repository.find_all()
        for index, user in enumerate(users):
            choices.append((str(user.id), user.email))
        self.fields['user'] = ChoiceField(choices=choices, required=False,
                                            widget=forms.Select(attrs={'class': 'form-select'}))
        dashboard_user_sensors = {}
        for user in users:
            if hasattr(user, 'dashboard_sensor'):
                dashboard_user_sensors[user.dashboarduser.get_sensor_id()] = user.dashboarduser.get_user().email
        choices = [("", "-")]
        for index, sensor in sensor_repository.find_all().items():
            if sensor.get_id() in dashboard_user_sensors:
                continue
            choices.append((str(index), str(index)))
        self.fields['sensor'] = ChoiceField(choices=choices, required=False,
                                            widget=forms.Select(attrs={'class': 'form-select'}))

    user = forms.ChoiceField()
    sensor = forms.ChoiceField(required=False)
