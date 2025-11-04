from django import forms
from django.forms.fields import ChoiceField
from dashboard_meet_je_stad.repository.sensor_utrecht_repository import SensorUtrechtRepository


class DashboardForm(forms.Form):

    def __init__(self, *args, **kwargs):
        is_inactive = kwargs.pop('is_inactive')
        repository = SensorUtrechtRepository()
        rows = repository.get()
        choices = [("", "-")]
        for index, row in rows.items():
            if is_inactive == 'off' and row[18] == '':
                choices.append((index, index))
            elif is_inactive == 'on':
                choices.append((index, index))
        super().__init__(*args, **kwargs)
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
