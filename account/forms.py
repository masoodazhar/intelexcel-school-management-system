from django import forms
from .models import InvoiceAmount, InvoiceDetail
from django.utils import timezone

class SearchExpenseIncome(forms.Form):
    date = forms.CharField(
        label='Select Date ',
        widget=forms.TextInput(attrs={
        'class': 'date ',
        'value': timezone.now().strftime('%Y-%m-%d')
    }))


class InvoiceAmountForm(forms.ModelForm):
    # fee_type = forms.CharField(widget=forms.TextInput(attrs={
    #     'name': 'fee_type'
    # }))
    module_holder = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'hidden'
    }))
    class Meta:
        model = InvoiceAmount
        fields = '__all__'


class InvoiceDetailForm(forms.ModelForm):
    date = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'date'
    }))
    module_holder = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'hidden'
    }))
    
    class Meta:
        model = InvoiceDetail
        fields = '__all__'
