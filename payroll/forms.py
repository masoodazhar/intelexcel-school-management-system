from django import forms
from .models import Teacher, Salary, EmployeeAttendance, Schedual
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

class FeeDefSerchForm(forms.Form):

    seacher_date = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'date seacher_date',
                'value': timezone.now().strftime('%Y-%m-%d')
            }
        )
    )


class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = [
            'employee_name',
            'Salary_date',
            'Salary_release_date',
            'salary',
            'payment_method',
            'advance_detected',
            'bonus',
            'other',
            'details'
        ]

class TeacherForm(UserCreationForm):
    class Meta:
        model = Teacher
        fields = [
        'first_name',
        'last_name',
        'date_of_birth',
        'religion',
        'Phone',
        'designation',
        'date_of_join',
        'photo',
        'gender',
        'position',
        'time_schedual',
        'address',
        'email',
        'username',
        'password1',
        'password2'
        # 'password1'
    ]


class EmployeeAttendanceForm(forms.ModelForm):

    # def __init__(self, user, *args, **kwargs):
    #     employee_name = 

    class Meta:
        model = EmployeeAttendance
        fields = [
            'employee_name',
            'date',
            'time_in',
            'time_out',
        ]

class SchedualForm(forms.ModelForm):
    """
    docstring
    """
    class Meta:
        model = Schedual
        fields = [
            'time_in',
            'time_out'
        ]