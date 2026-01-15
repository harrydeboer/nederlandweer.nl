from django import forms
from django.forms.fields import ChoiceField
from django.forms.fields import IntegerField


class DashboardForm(forms.Form):

    def __init__(self, *args, **kwargs):
        begin_year = kwargs.pop('begin_year')
        end_year = kwargs.pop('end_year')
        if len(args[0]) > 0:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(**kwargs)
        self.fields['begin_year'] = IntegerField(initial=begin_year)
        self.fields['end_year'] = IntegerField(initial=end_year)

    choices = [
        ("", "-"),
        ('temperature-day', 'Temperatuur dag'),
        ('temperature-year', 'Temperatuur jaar'),
        ('amount_rain', 'Regen hoeveelheid'),
        ('perc_rain', 'Regen percentage'),
        ('perc_sunshine', 'Zon percentage'),
        ('wind_speed', 'Wind snelheid'),
        ('wind_speed_va', 'Wind richting'),
        ('tropical', 'Tropische dagen'),
        ('extreme', 'Extreem'),
    ]
    type = ChoiceField(choices=choices, required=False,
                widget=forms.Select(attrs={'class': 'form-select'}))

    begin_year = forms.IntegerField()

    end_year = forms.IntegerField()
