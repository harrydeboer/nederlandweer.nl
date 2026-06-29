from django import forms


class DatasetForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    start = forms.DateTimeField(input_formats = ['Y-d-m,HH:mm:ss'])
    end = forms.DateTimeField(input_formats = ['Y-d-m,HH:mm:ss'])