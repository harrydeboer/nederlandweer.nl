from django import forms
from django.core.validators import FileExtensionValidator


class MailchimpForm(forms.Form):
    file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=["xlsx"])])
