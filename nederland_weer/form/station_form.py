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
        self.fields['begin_year'].initial = station.get_begin_year()
        self.fields['end_year'].initial = station.get_end_year()
        self.fields['begin_year_min_temp'].initial = station.get_begin_year_min_temp()
        self.fields['begin_year_mean_temp'].initial = station.get_begin_year_mean_temp()
        self.fields['begin_year_max_temp'].initial = station.get_begin_year_mean_temp()
        self.fields['begin_year_wind_direction'].initial = station.get_begin_year_wind_direction()
        self.fields['begin_year_wind_speed'].initial = station.get_begin_year_wind_speed()
        self.fields['begin_year_wind_speed_va'].initial = station.get_begin_year_wind_speed_va()
        self.fields['begin_year_perc_sunshine'].initial = station.get_begin_year_perc_sunshine()
        self.fields['begin_year_perc_rain'].initial = station.get_begin_year_perc_rain()
        self.fields['begin_year_amount_rain'].initial = station.get_begin_year_amount_rain()
        self.fields['longitude'].initial = station.get_longitude()
        self.fields['latitude'].initial = station.get_latitude()

    id = forms.IntegerField()
    name = forms.CharField()
    begin_year = forms.IntegerField()
    end_year = forms.IntegerField()
    begin_year_min_temp = forms.IntegerField()
    begin_year_mean_temp = forms.IntegerField()
    begin_year_max_temp = forms.IntegerField()
    begin_year_wind_direction = forms.IntegerField()
    begin_year_wind_speed = forms.IntegerField()
    begin_year_wind_speed_va = forms.IntegerField()
    begin_year_perc_sunshine = forms.IntegerField()
    begin_year_perc_rain = forms.IntegerField()
    begin_year_amount_rain = forms.IntegerField()
    longitude = forms.FloatField()
    latitude = forms.FloatField()
