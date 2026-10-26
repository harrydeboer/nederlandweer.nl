from django import forms


class StationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        station = kwargs['station']
        kwargs.pop('station')
        if len(args[0]) > 0:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(**kwargs)
        self.fields['id'].initial = station.get_id()
        self.fields['name'].initial = station.get_name()
        self.fields['longitude'].initial = station.get_longitude()
        self.fields['latitude'].initial = station.get_latitude()

    id = forms.IntegerField()
    name = forms.CharField()
    longitude = forms.FloatField()
    latitude = forms.FloatField()
