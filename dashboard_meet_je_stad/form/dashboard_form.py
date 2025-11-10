from django import forms
from django.forms.fields import ChoiceField
from dashboard_meet_je_stad.repository.sensor_utrecht_repository import SensorUtrechtRepository


class DashboardForm(forms.Form):

    def __init__(self, *args, **kwargs):
        pm = kwargs.pop('pm')
        sensors = kwargs.pop('sensors')
        inactive = kwargs.pop('inactive')
        repository = SensorUtrechtRepository()
        if sensors == {}:
            sensors_utrecht = repository.get()
        else:
            sensors_utrecht = repository.get(pm=pm)
        choices = [("", "-")]
        if inactive:
            for index, row in sensors_utrecht.items():
                choices.append((index, index))
        else:
            for index, sensor in sensors.items():
                choices.append((index, index))
        if len(args[0]) > 0:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(**kwargs)
        self.fields['sensor'] = ChoiceField(choices=choices, required=False,
                                            widget=forms.Select(attrs={'class': 'form-select'}))

    inactive = forms.BooleanField(label='Inactief', required=False,
                                  widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    pm = forms.BooleanField(label='Alleen fijnstof', required=False,
                            widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    choices = [
        ('temperature', 'Temperatuur'),
        ('humidity', 'Luchtvochtigheid'),
        ('pm25', 'Fijnstof 2,5'),
        ('pm10', 'Fijnstof 10'),
    ]
    type = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        choices=choices,
        initial='temperature'
    )

    sensor = forms.ChoiceField()
