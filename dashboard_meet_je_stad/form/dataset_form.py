from email.policy import default

from django import forms


class DatasetForm(forms.Form):

    def __init__(self, *args, **kwargs):
        if len(args[0]) > 0:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(**kwargs)

    start = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': 'yyyy-mm-dd,HH:mm:ss'}),
                                input_formats = ['Y-d-m,HH:mm:ss'], label='Begin')
    end = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': 'yyyy-mm-dd,HH:mm:ss'}),
                              input_formats = ['Y-d-m,HH:mm:ss'], label='Eind')
    ids = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'ids'}))

    particulate_matter_only = forms.BooleanField(initial=False, required=False, label='Alleen fijnstof sensors')

    active_only = forms.BooleanField(initial=False, required=False, label='Alleen actieve sensors')

    cutoff_temp = forms.BooleanField(initial=True, required=False, label='Afkap temperatuur')

    cutoff_temp_min = forms.FloatField(initial=-25, required=False, label='Min temperatuur')

    cutoff_temp_max = forms.FloatField(initial=70, required=False, label='Max temperatuur')

    cutoff_pm25 = forms.BooleanField(initial=True, required=False, label='Afkap fijnstof 2.5')

    cutoff_pm25_min = forms.FloatField(initial=0, required=False, label='Min fijnstof 2.5')

    cutoff_pm25_max = forms.FloatField(initial=250, required=False, label='Max fijnstof 2.5')

    cutoff_pm10 = forms.BooleanField(initial=True, required=False, label='Afkap fijnstof 10')

    cutoff_pm10_min = forms.FloatField(initial=0, required=False, label='Min fijnstof 10')

    cutoff_pm10_max = forms.FloatField(initial=250, required=False, label='Max fijnstof 10')
