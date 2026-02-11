from django import forms


class LoginForm(forms.Form):

    def __init__(self, *args, **kwargs):
        if len(args[0]) > 0:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(**kwargs)

    username = forms.CharField()

    password = forms.CharField(widget=forms.PasswordInput())
