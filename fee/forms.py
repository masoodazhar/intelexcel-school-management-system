from django import forms
from student.models import Admission, Classes, Section
from django.utils import timezone
import datetime


years = []

current_year = timezone.now().strftime("%Y")

for i in range(2005, int(current_year)+2):
    years.append(
        (i, i)
    )



class SearchChallan(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(SearchChallan, self).__init__(*args, **kwargs)
        # self.fields['class_name'].widget.attrs={'class': 'basic-multiple'}
        self.fields['classes'].widget.attrs={'class': 'basic-multiple'}
        self.fields['admission_section'].widget.attrs={'class': 'basic-multiple'}
        self.fields['classes'].queryset = Classes.objects.filter(module_holder=user)
        self.fields['admission_section'].queryset = Section.objects.filter(module_holder=user)

    issue_date = forms.DateField(required=False, widget=forms.TextInput(
        attrs={
            'class': 'date',
            'value': timezone.now().strftime('%Y-%m-%d')
        }
    ))
    due_date = forms.DateField(required=False, widget=forms.TextInput(
        attrs={
            'class': 'date',
            'value': (timezone.now()+datetime.timedelta(7)).strftime('%Y-%m-%d')
        }
    ))
    fee_month = forms.CharField(max_length=50 ,required=False, widget=forms.TextInput(
        attrs={
            'type': 'month',
            'value': timezone.now().strftime('%Y-%m')
        }
    ))
    year = forms.ChoiceField(choices=years, widget=forms.Select(
        attrs = {
            'class': 'year',
            'value': timezone.now().strftime('%Y')
        }
    ))
    classes = forms.ModelChoiceField(queryset=Classes.objects.all())
    admission_section = forms.ModelChoiceField(queryset=Section.objects.all())
   
