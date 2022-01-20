from django import forms
from academic.models import Classes, Section, Subject
from .models import Admission, StudentMark, Attendance, ExamEmail, CalculateResults
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.utils import timezone


class CalculateResultsForm(forms.ModelForm):
    class Meta:
        model = CalculateResults
        fields = '__all__'

class ExamEmailForm(forms.ModelForm):
    class Meta:
        model = ExamEmail
        fields = '__all__'

        
class TrophiesForm(ModelForm):
    # admission_class = forms.ModelMultipleChoiceField(queryset=Gun.objects.filter(user__id=1))

    def __init__(self, user, *args, **kwargs):
        super(TrophiesForm, self).__init__(*args, **kwargs)
        # print(user,'================h=hh===h=h=h==h=====h=h=h=')
        self.fields['admission_class'].queryset = Classes.objects.filter(module_holder=user)

    class Meta:
        model = Admission
        fields = [
            'admission_date',
            'admission_class',
            'admission_section',
            'admission_registration',
            'name_of_student',
            'father_name',
            'father_cnic',
            'cast',
            'father_profession',
            'date_of_birth',
            'contact',
            'address',
            'gender',
            'recieve_admissin_fee_with_admission',
            'monthly_tution_fee',
            'concession_fee',
            'annual_fund',
            'free_student',
            'photo'
        ]

    
# Create your views here.
class AttendanceForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        print(user,'================h=hh===h=h=h==h=====h=h=h=')
        # self.fields['student_id'].queryset = Admission.objects.filter(module_holder=user)
        self.fields['section'].widget.attrs={'class': 'basic-multiple'}
        self.fields['section'].queryset = Section.objects.filter(module_holder=user)
        self.fields['classes'].widget.attrs['class']='basic-multiple'
        self.fields['classes'].queryset = Classes.objects.filter(module_holder=user)
        
    remarks = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 20}))
    # section = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # classes = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    from_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'class': 'date', 'value': timezone.now().strftime('%Y-%m-%d')}))
    to_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'class': 'date', 'value':  timezone.now().strftime('%Y-%m-%d')}))
    registration = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # attendance_selection = forms.CharField(widget = forms.RadioSelect())
    
    class Meta:
        model = Attendance
        fields = '__all__'


class StudentMarkSearchForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(StudentMarkSearchForm, self).__init__(*args, **kwargs)
        self.fields['class_name'].widget.attrs={'class': 'basic-multiple'}
        # self.fields['section'].queryset = Section.objects.filter(module_holder=user)
        # self.fields['subject'].queryset = Subject.objects.filter(module_holder=user)
       
        if args:
            self.fields['subject'].queryset = Subject.objects.filter(module_holder=user,class_name__contains=args[0]['class_name'] )
            
        else:
            self.fields['subject'].queryset = Subject.objects.filter(module_holder=user )

        self.fields['class_name'].queryset = Classes.objects.filter(module_holder=user)
        self.fields['section'].queryset = Section.objects.filter(module_holder=user )
        


    class_name = forms.ModelChoiceField(queryset=Classes.objects.filter())
    section = forms.ModelChoiceField(queryset=Section.objects.filter())
    subject = forms.ModelChoiceField(queryset=Subject.objects.filter())


class StudentMarkForm(forms.ModelForm):
    exam = forms.CharField(widget=forms.TextInput(attrs={'class': 'class_exam'})) 
    attendance = forms.CharField(widget=forms.TextInput(attrs={'class': 'class_attendance'})) 
    class_test = forms.CharField(widget=forms.TextInput(attrs={'class': 'class_class_test'})) 
    assignment = forms.CharField(widget=forms.TextInput(attrs={'class': 'class_assignment'})) 
    
    class Meta:
        model = StudentMark
        fields = '__all__'




class AdmissionForm(forms.ModelForm):
    # admission_class = forms.ModelChoiceField(queryset=Classes.objects.filter(module_holder='masood1'))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    # def __init__(self, user, *args, **kwargs):
    #     super(TrophiesForm, self).__init__(*args, **kwargs)
    #     self.fields['used_his'].queryset = User.objects.filter(pk = user.id)
   
    # def __init__(self,  *args, **kwargs):
    #      self.user = kwargs.pop('user',None)
    #      super(AdmissionForm, self).__init__(*args, **kwargs)
    #      print(self.users.user,'=====s==s=da=sd=sd=as=d=sd=s=da=sd=sa=ds=d=sd==')
    #      self.fields['admission_class'].queryset = Classes.objects.filter(module_holder='masood1')

    class Meta:
        model = Admission
        fields = [
            'admission_date',
            'admission_class',
            'admission_section',
            'admission_registration',
            'name_of_student',
            'father_name',
            'father_cnic',
            'cast',
            'father_profession',
            'date_of_birth',
            'contact',
            'address',
            'gender',
            'recieve_admissin_fee_with_admission',
            'monthly_tution_fee',
            'concession_fee',
            'annual_fund',
            'free_student',
            'photo',
            'father_email_address',
            'Student_email_address',
            'password'
        ]