from django import forms
from django.forms.fields import ChoiceField, DateField
import datetime


class DashboardForm(forms.Form):

    def __init__(self, *args, **kwargs):
        stations = kwargs.pop('stations')
        if len(args[0]) > 0:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(**kwargs)
        choices = []
        for index, station in stations.items():
            choices.append((station.get_id(), station.get_name()))
        self.fields['station'] = ChoiceField(initial='260', choices=choices, required=True,
                                             widget=forms.Select(attrs={'class': 'form-select'}))
        self.fields['begin_year'] = DateField(initial='01-01-1901',
                                                 widget=forms.DateInput(attrs={'class': 'form-control',
                                                                               'placeholder': 'dd-mm-jjjj'},
                                                                        format="%d-%m-%Y"), input_formats=["%d-%m-%Y"])
        self.fields['end_year'] = DateField(initial=datetime.datetime.now(),
                                               widget=forms.DateInput(attrs={'class': 'form-control',
                                                                             'placeholder': 'dd-mm-jjjj'},
                                                                      format="%d-%m-%Y"), input_formats=["%d-%m-%Y"])

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
    component = ChoiceField(choices=choices, required=True,
                widget=forms.Select(attrs={'class': 'form-select'}))

    station = forms.ChoiceField()

    begin_year = forms.DateField()

    end_year = forms.DateField()
