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
        self.fields['begin_year'] = IntegerField(initial=begin_year,
                                                 widget=forms.NumberInput(attrs={'class': 'form-control'}))
        self.fields['end_year'] = IntegerField(initial=end_year,
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

    begin_year = forms.IntegerField()

    end_year = forms.IntegerField()
