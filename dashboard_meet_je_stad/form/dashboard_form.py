from django import forms
from django.forms.fields import ChoiceField


class DashboardForm(forms.Form):

    def __init__(self, *args, **kwargs):
        sensors = kwargs.pop('sensors')
        inactive = kwargs.pop('inactive')
        choices = [("", "-")]
        for index, sensor in sensors.items():
            if not inactive and not sensor.is_active:
                continue
            choices.append((str(index), str(index)))
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

    choices_graph = [
        ('24hour', '24 uur'),
        ('3month', '3 maanden'),
    ]
    interval = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        choices=choices_graph,
        initial='24hour'
    )

    sensor = forms.ChoiceField()
