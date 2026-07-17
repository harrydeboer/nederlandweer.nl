from django import forms

from dashboard_meet_je_stad.service.cleanup_service import CleanupService


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
    ids = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': 'Als dit veld leeg is worden alle ids van Utrecht geselecteerd', 'cols': 100, 'rows': 3}))

    particulate_matter_only = forms.BooleanField(initial=False, required=False, label='Alleen fijnstof sensors')

    active_only = forms.BooleanField(initial=False, required=False, label='Alleen actieve sensors')

    cutoff_temp = forms.BooleanField(initial=CleanupService.cleanup_default['cutoff_temp']['is_on'],
                                     required=False, label='Afkap temperatuur')

    cutoff_temp_min = forms.FloatField(initial=CleanupService.cleanup_default['cutoff_temp']['min'],
                                       required=False, label='Min temperatuur')

    cutoff_temp_max = forms.FloatField(initial=CleanupService.cleanup_default['cutoff_temp']['max'],
                                       required=False, label='Max temperatuur')

    cutoff_pm25 = forms.BooleanField(initial=CleanupService.cleanup_default['cutoff_pm25']['is_on'],
                                     required=False, label='Afkap fijnstof 2.5')

    cutoff_pm25_min = forms.FloatField(initial=CleanupService.cleanup_default['cutoff_pm25']['min'],
                                       required=False, label='Min fijnstof 2.5')

    cutoff_pm25_max = forms.FloatField(initial=CleanupService.cleanup_default['cutoff_pm25']['max'],
                                       required=False, label='Max fijnstof 2.5')

    cutoff_pm10 = forms.BooleanField(initial=CleanupService.cleanup_default['cutoff_pm10']['is_on'],
                                     required=False, label='Afkap fijnstof 10')

    cutoff_pm10_min = forms.FloatField(initial=CleanupService.cleanup_default['cutoff_pm10']['min'],
                                       required=False, label='Min fijnstof 10')

    cutoff_pm10_max = forms.FloatField(initial=CleanupService.cleanup_default['cutoff_pm10']['max'],
                                       required=False, label='Max fijnstof 10')

    def get_requested_cleanup(self) -> dict:
        cleanup = CleanupService.cleanup_default
        for key, value in CleanupService.cleanup_default.items():
            for key_param, value_param in value.items():
                if key_param == 'is_on':
                    cleanup[key][key_param] = self[key].value()
                else:
                    cleanup[key][key_param] = self.set_value_to_number(self[key + '_' + key_param].value(), True)

        return cleanup

    def set_value_to_number(self, value: str, return_float: bool) -> float|int|None:
        if value == '':
            return None

        if return_float:
            return float(value)

        return int(value)
