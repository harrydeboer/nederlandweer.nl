from django import forms


class DatasetForm(forms.Form):

    def __init__(self, *args, **kwargs):
        if len(args[0]) > 0:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(**kwargs)

    cleanup = {'cutoff_temp': [True, -25, 70],
               'cutoff_pm25': [True, 0, 250],
               'cutoff_pm10': [True, 0, 250]}

    start = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': 'yyyy-mm-dd,HH:mm:ss'}),
                                input_formats = ['Y-d-m,HH:mm:ss'], label='Begin')
    end = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': 'yyyy-mm-dd,HH:mm:ss'}),
                              input_formats = ['Y-d-m,HH:mm:ss'], label='Eind')
    ids = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': 'Als dit veld leeg is worden alle ids van Utrecht geselecteerd', 'cols': 100, 'rows': 3}))

    particulate_matter_only = forms.BooleanField(initial=False, required=False, label='Alleen fijnstof sensors')

    active_only = forms.BooleanField(initial=False, required=False, label='Alleen actieve sensors')

    cutoff_temp = forms.BooleanField(initial=True, required=False, label='Afkap temperatuur')

    cutoff_temp_min = forms.FloatField(initial=cleanup['cutoff_temp'][1],
                                       required=False, label='Min temperatuur')

    cutoff_temp_max = forms.FloatField(initial=cleanup['cutoff_temp'][2],
                                       required=False, label='Max temperatuur')

    cutoff_pm25 = forms.BooleanField(initial=True, required=False, label='Afkap fijnstof 2.5')

    cutoff_pm25_min = forms.FloatField(initial=cleanup['cutoff_pm25'][1],
                                       required=False, label='Min fijnstof 2.5')

    cutoff_pm25_max = forms.FloatField(initial=cleanup['cutoff_pm25'][2],
                                       required=False, label='Max fijnstof 2.5')

    cutoff_pm10 = forms.BooleanField(initial=True, required=False, label='Afkap fijnstof 10')

    cutoff_pm10_min = forms.FloatField(initial=cleanup['cutoff_pm10'][1],
                                       required=False, label='Min fijnstof 10')

    cutoff_pm10_max = forms.FloatField(initial=cleanup['cutoff_pm10'][2],
                                       required=False, label='Max fijnstof 10')

    def get_populated_cleanup(self) -> dict:

        return {'cutoff_temp': [self['cutoff_temp'].value(),
                         float(self['cutoff_temp_min'].value()),
                         float(self['cutoff_temp_max'].value())],
         'cutoff_pm25': [self['cutoff_pm25'].value(),
                         float(self['cutoff_pm25_min'].value()),
                         float(self['cutoff_pm25_max'].value())],
         'cutoff_pm10': [self['cutoff_pm10'].value(),
                         float(self['cutoff_pm10_min'].value()),
                         float(self['cutoff_pm10_max'].value())]}
