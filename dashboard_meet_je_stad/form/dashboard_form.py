from django import forms
from django.forms.fields import ChoiceField


class DashboardForm(forms.Form):

    """The sensors are retrieved from the kwargs and then removed from kwargs.
    The choices of the sensor are added to the sensor field.
    """
    def __init__(self, *args, **kwargs):
        sensors = kwargs['sensors']
        inactive = kwargs['inactive']
        pm = kwargs['pm']
        kwargs.pop('sensors')
        kwargs.pop('inactive')
        kwargs.pop('pm')
        if len(args[0]) > 0:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(**kwargs)
        choices = [("", "-")]
        for index, sensor in sensors.items():
            choices.append((str(index), str(index)))
        self.fields['sensor'] = ChoiceField(choices=choices, required=False,
                                            widget=forms.Select(attrs={'class': 'form-select'}))
        if inactive:
            self.fields['inactive'].initial = inactive
        if pm:
            self.fields['pm'].initial = pm

    inactive = forms.BooleanField(label='Inactief', required=False,
                                  widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    pm = forms.BooleanField(label='Alleen fijnstof', required=False,
                            widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    choices = [
        ('temperature', 'Temperatuur'),
        ('humidity', 'Luchtvochtigheid'),
        ('pm25', 'Fijnstof 2,5 µm'),
        ('pm10', 'Fijnstof 10 µm'),
    ]
    type = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        choices=choices,
        initial='temperature'
    )

    choices_graph = [
        ('24hour', '24 uur'),
        ('1month', '1 maand'),
    ]
    interval = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        choices=choices_graph,
        initial='24hour'
    )

    sensor = forms.ChoiceField()
