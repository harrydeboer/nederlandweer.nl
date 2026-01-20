from django import forms
from django.forms.fields import ChoiceField
from django.forms.fields import IntegerField


class DashboardForm(forms.Form):

    def __init__(self, *args, **kwargs):
        stations = kwargs.pop('stations')
        if len(args[0]) > 0:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(**kwargs)
        choices = []
        station_de_bilt = []
        for station in stations:
            choices.append((station[0], station[1]))
            if station[0] == '260':
                station_de_bilt = station
        self.fields['station'] = ChoiceField(initial='260', choices=choices, required=True,
                                             widget=forms.Select(attrs={'class': 'form-select'}))
        self.fields['begin_year'] = IntegerField(initial=station_de_bilt[2],
                                                 widget=forms.NumberInput(attrs={'class': 'form-control'}))
        self.fields['end_year'] = IntegerField(initial=station_de_bilt[3],
                                               widget=forms.NumberInput(attrs={'class': 'form-control'}))

    choices = [
        ("", "-"),
        ('temperature-day', 'Temperatuur dag'),
        ('temperature-year', 'Temperatuur jaar'),
        ('amount-rain', 'Regen hoeveelheid'),
        ('perc-rain', 'Regen percentage'),
        ('perc-sunshine', 'Zon percentage'),
        ('wind-speed', 'Wind snelheid'),
        ('wind-speed-va', 'Wind richting'),
        ('tropical', 'Tropische dagen'),
        ('extreme', 'Extreem'),
    ]
    type = ChoiceField(choices=choices, required=True,
                widget=forms.Select(attrs={'class': 'form-select'}))

    station = forms.ChoiceField()

    begin_year = forms.IntegerField()

    end_year = forms.IntegerField()
