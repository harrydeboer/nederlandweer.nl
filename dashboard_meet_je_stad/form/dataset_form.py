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

    particulate_matter_only = forms.BooleanField(initial=False, label='Alleen fijnstof sensors')

    active_only = forms.BooleanField(initial=False, label='Alleen actieve sensors')

    cutoff_temp = forms.BooleanField(initial=True, label='Afkap temperatuur')

    cutoff_pm25 = forms.BooleanField(initial=True, label='Afkap fijnstof 2.5')

    cutoff_pm10 = forms.BooleanField(initial=True, label='Afkap fijnstof 10')
