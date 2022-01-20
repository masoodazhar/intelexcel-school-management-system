from django import forms
from .models import Email

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = [
            'mail_from',
            'mail_to',
            'mail_cc',
            'subject',
            'message',
            'attachment',
            'module_holder'
        ]


