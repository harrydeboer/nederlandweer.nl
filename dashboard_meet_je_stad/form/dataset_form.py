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