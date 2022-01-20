from django import forms
# from .models import Teacher
# from django.contrib.auth.forms import UserCreationForm
from .models import Subject, Section, Classes

class ClassesForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(ClassesForm, self).__init__(*args, **kwargs)
        # self.fields['section'].queryset = Section.objects.filter(module_holder=user)
        # self.fields['subject'].queryset = Subject.objects.filter(module_holder=user)
        self.fields['section'].queryset = Section.objects.filter(module_holder=user )

    class Meta:
        model = Classes
        fields = ['section','class_name','class_number','fee','discount','note']

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['section_name']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = [
        'class_name',
        'subject_type',
        'pass_mark',
        'final_mark',
        'subject_name',
        'subject_code',
        'note'
        ]

# class TeacherForm(UserCreationForm):
#     class Meta:
#         model = Teacher
#         fields = [
#         'first_name',
#         'last_name',
#         'date_of_birth',
#         'religion',
#         'Phone',
#         'designation',
#         'date_of_join',
#         'photo',
#         'gender',
#         'salary',
#         'address',
#         'email',
#         'username',
#         'password1',
#         'password2'
#         # 'password1'
#     ]