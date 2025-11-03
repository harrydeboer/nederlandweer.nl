from django import forms


class DashboardForm(forms.Form):
    inactive = forms.BooleanField(label='Inactief', required=False)
    pm = forms.BooleanField(label='Alleen fijnstof', required=False)
    CHOICES = [
        ('temperature', 'Temperatuur'),
        ('humidity', 'Luchtvochtigheid'),
        ('pm25', 'Fijnstof 2,5'),
        ('pm10', 'Fijnstof 10'),
    ]
    type = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES,
    )
