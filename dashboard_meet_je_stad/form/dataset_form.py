from django import forms


class DatasetForm(forms.Form):

    def __init__(self, *args, **kwargs):
        if len(args[0]) > 0:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(**kwargs)

    cleanup_default = {'cutoff_temp': {'is_on': True, 'min': -25, 'max': 70},
               'cutoff_pm25': {'is_on': True, 'min': 0, 'max': 250},
               'cutoff_pm10': {'is_on': True, 'min': 0, 'max': 250}}

    start = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': 'yyyy-mm-dd,HH:mm:ss'}),
                                input_formats = ['Y-d-m,HH:mm:ss'], label='Begin')
    end = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': 'yyyy-mm-dd,HH:mm:ss'}),
                              input_formats = ['Y-d-m,HH:mm:ss'], label='Eind')
    ids = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': 'Als dit veld leeg is worden alle ids van Utrecht geselecteerd', 'cols': 100, 'rows': 3}))

    particulate_matter_only = forms.BooleanField(initial=False, required=False, label='Alleen fijnstof sensors')

    active_only = forms.BooleanField(initial=False, required=False, label='Alleen actieve sensors')

    cutoff_temp = forms.BooleanField(initial=True, required=False, label='Afkap temperatuur')

    cutoff_temp_min = forms.FloatField(initial=cleanup_default['cutoff_temp']['min'],
                                       required=False, label='Min temperatuur')

    cutoff_temp_max = forms.FloatField(initial=cleanup_default['cutoff_temp']['max'],
                                       required=False, label='Max temperatuur')

    cutoff_pm25 = forms.BooleanField(initial=True, required=False, label='Afkap fijnstof 2.5')

    cutoff_pm25_min = forms.FloatField(initial=cleanup_default['cutoff_pm25']['min'],
                                       required=False, label='Min fijnstof 2.5')

    cutoff_pm25_max = forms.FloatField(initial=cleanup_default['cutoff_pm25']['max'],
                                       required=False, label='Max fijnstof 2.5')

    cutoff_pm10 = forms.BooleanField(initial=True, required=False, label='Afkap fijnstof 10')

    cutoff_pm10_min = forms.FloatField(initial=cleanup_default['cutoff_pm10']['min'],
                                       required=False, label='Min fijnstof 10')

    cutoff_pm10_max = forms.FloatField(initial=cleanup_default['cutoff_pm10']['max'],
                                       required=False, label='Max fijnstof 10')

    def get_requested_cleanup(self) -> dict:

        return {'cutoff_temp': {'is_on': self['cutoff_temp'].value(),
                         'min': self.set_value(self['cutoff_temp_min'].value()),
                         'max': self.set_value(self['cutoff_temp_max'].value())},
         'cutoff_pm25': {'is_on': self['cutoff_pm25'].value(),
                         'min': self.set_value(self['cutoff_pm25_min'].value()),
                         'max': self.set_value(self['cutoff_pm25_max'].value())},
         'cutoff_pm10': {'is_on': self['cutoff_pm10'].value(),
                         'min': self.set_value(self['cutoff_pm10_min'].value()),
                         'max': self.set_value(self['cutoff_pm10_max'].value())}}

    def set_value(self, value: float|str) -> float| str:
        if value == '':
            return ''

        return float(value)
