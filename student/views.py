from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, DetailView, View
from django.views.generic.edit import FormView
from django import forms
from django.forms import ModelForm
from academic.models import Section, Classes, Routine, Subject
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Q
from django.utils import timezone
import datetime
from calendar import monthrange
from .models import Attendance, Admission, StudentMark, MarkDistribution, Exams, ExamEmail, CalculateResults
from academic.forms import ClassesForm, SectionForm
from .forms import StudentMarkSearchForm, StudentMarkForm, AdmissionForm, TrophiesForm, AttendanceForm, ExamEmailForm, CalculateResultsForm
import json
# from django.http import JsonResponse
# Student section
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from home.decorators import allowed_users
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from payroll.models import Teacher
from fee.models import Voucher
from django.contrib import messages
from home.models import SchoolProfile
from django.contrib.auth.hashers import make_password


admissionfields = [
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
            'Student_email_address',
            'father_email_address',
            'password'
        ]

current_month = str(timezone.now().strftime('%m/%Y'))

all_months = ['01','02','03','04','05','06','07','08','09','10','11','12']

current_year = timezone.now().strftime('%Y')
fee_year = timezone.now().strftime('%Y')

start_year=2020

def convert_month_into_string(number):
    if str(number) == '01':
        return 'Jan'
    elif str(number) == '02':
        return 'Feb'
    elif str(number) == '03':
        return 'Mar'
    elif str(number) == '04':
        return 'Apr'
    elif str(number) == '05':
        return 'May'
    elif str(number) == '06':
        return 'Jun'
    elif str(number) == '07':
        return 'Jul'
    elif str(number) == '08':
        return 'Aug'
    elif str(number) == '09':
        return 'Sep'
    elif str(number) == '10':
        return 'Oct'
    elif str(number) == '11':
        return 'Nov'
    elif str(number) == '12':
        return 'Dec'
    else:
        return 'invalid'

def convert_month_2_string(number):
    if number == 1:
        return 'Jan'
    elif number == 2:
        return 'Feb'
    elif number == 3:
        return 'Mar'
    elif number == 4:
        return 'Apr'
    elif number == 5:
        return 'May'
    elif number == 6:
        return 'Jun'
    elif number == 7:
        return 'Jul'
    elif number == 8:
        return 'Aug'
    elif number == 9:
        return 'Sep'
    elif number == 10:
        return 'Oct'
    elif number == 11:
        return 'Nov'
    elif number == 12:
        return 'Dec'
    else:
        return 'invalid'


def attendance_converter(attendance,dates):
    y,m,d = str(dates).split(" ")[0].split('-')    
    if attendance == '1':
        return 'P'
    elif attendance == '2':
        return 'A'
    elif attendance == '3':
        return 'L'
    elif attendance == '4':
        return 'L-I'
    elif attendance == '5':
        return 'O' 
    else:
        # return 's'
        checking_date = datetime.date(int(y),int(m),int(d))
        current_date = datetime.date.today()
        if_checkdate_less_current = checking_date < current_date
        if if_checkdate_less_current:
            return 'H'
        else:
            return 'N/A'


def generate_reg(id):
    id = int(id)+1
    final = ''
    id = str(id)
    if len(id)<2:
        final = '00000'+id
    elif len(id)<3:
        final = '0000'+id
    elif len(id)<4:
        final = '000'+id
    elif len(id)<5:
        final = '00'+id
    elif len(id)<6:
        final = '0'+id
    else:
         final = id
    return final
    
def my_trophies(request, *args, **kwargs):
    user = request.user
    form = TrophiesForm(user)

    return render(request, 'sample.html', {'form': form})
 

def get_fee(request):
    print(len(request.GET),'==================')
    fee=0
    discount=0
    if request.GET:
        class_object = Classes.objects.filter(pk=request.GET.get('id')).first()
        fee = class_object.fee
        discount = class_object.discount
    context = {
            'fee': fee,
            'discount': discount
    }
    return JsonResponse(context)

def get_already_marks(request):
    if request.user.is_staff:
        module_holder = request.user.username
    else:
        this_holder = Teacher.objects.get(user_ptr_id=request.user.id)
        module_holder = this_holder.module_holder

    marks = dict()
    class_id = request.GET.get('class_name')
    subject_id = request.GET.get('subject_name')
    data = MarkDistribution.objects.filter(class_name=class_id,subject_name=subject_id, module_holder=module_holder).first()
    subject_object = Subject.objects.filter(pk=subject_id).first()
  
    if data:
        marks.update({
            'exam': data.exam,
            'attendance': data.attendance,
            'class_test': data.class_test,
            'assignment': data.assignment,
            'passing_marks': subject_object.pass_mark,
            'final_marks': subject_object.final_mark
        })
    print(marks)
    return JsonResponse(marks)


def get_subject_by_class(request):
    class_name = request.GET.get('class_name')
    subjects = Subject.objects.filter(class_name__contains=class_name)
    
    data = []
    for subject in subjects:
        data.append({
            'name': subject.subject_name,
            'id': subject.pk
        })

    return JsonResponse({'data':data})

@login_required
# @allowed_users('view_student')
def StudentView(request):
    template_name = ''
    monthly_chart_data =[] 

    if request.user.is_staff:
        module_holder = request.user.username
    else:
        this_holder = Teacher.objects.get(user_ptr_id=request.user.id)
        module_holder = this_holder.module_holder

    for month in all_months:
        year_month = str(current_year)+'-'+str(month) 
        students_monthly = Admission.objects.filter(module_holder=module_holder, admission_date__startswith=year_month).count()
        present_monthly = Attendance.objects.filter(module_holder=module_holder, attendance_selection=1, date__startswith=year_month).count()
        absent_monthly = Attendance.objects.filter(module_holder=module_holder, attendance_selection=2, date__startswith=year_month).count()
        leave_monthly = Attendance.objects.filter(module_holder=module_holder, attendance_selection=3, date__startswith=year_month).count()
        latein_monthly = Attendance.objects.filter(module_holder=module_holder, attendance_selection=4, date__startswith=year_month).count()
        dropout_monthly = Admission.objects.filter(module_holder=module_holder, status_date__startswith=year_month, status=0).count()
        monthly_chart_data.append({
            'date': year_month+'-01',
            'student': students_monthly,
            'present': present_monthly,
            'absent': absent_monthly,
            'leave': leave_monthly,
            'latein': latein_monthly,
            'dropout': dropout_monthly
        })


    students_yearly = Admission.objects.filter(module_holder=module_holder, admission_date__startswith=current_year).count()
    present_yearly = Attendance.objects.filter(module_holder=module_holder, attendance_selection=1, date__startswith=current_year).count()   
    absent_yearly = Attendance.objects.filter(module_holder=module_holder, attendance_selection=2, date__startswith=current_year).count()    
    leave_yearly = Attendance.objects.filter(module_holder=module_holder, attendance_selection=3, date__startswith=current_year).count() 
    latin_yearly = Attendance.objects.filter(module_holder=module_holder, attendance_selection=4, date__startswith=current_year).count() 
    dropout_yearly = Admission.objects.filter(module_holder=module_holder, status_date__startswith=current_year, status=0).count() 

    chart_data_yearly = {
        'students_yearly': students_yearly,
        'present_yearly': present_yearly,
        'absent_yearly': absent_yearly,
        'leave_yearly': leave_yearly,
        'latin_yearly': latin_yearly,
        'dropout_yearly': dropout_yearly

    }
    context = {
        'chart_data_monthly': json.dumps(monthly_chart_data),
        'chart_data_yearly': chart_data_yearly,
        'current_year': current_year
    }
    return render(request,'student/student_view.html', context)


# STUDENT MARKS START HERE
class StudentMarkSearch(FormView):
    template_name= 'student/mark_search.html'  
    # form_class = StudentMarkSearchForm() 
    
    def get(self, request):
        mark_ditribution_header=[]
        if request.user.is_staff:
            module_holder = request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=request.user.id)
            module_holder = this_holder.module_holder

        collect_student_form_with_data = []
        form = StudentMarkSearchForm(module_holder)
       
        context = {
            'mark_ditribution_header':mark_ditribution_header,
            'collect_student_form_with_data': collect_student_form_with_data,
            'form': form
        }
        return render(request, self.template_name, context)

    def get_form(self, **kwargs):
        form = super(StudentMarkSearch, self).get_form(**kwargs)  
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        form.fields['class_name'].queryset = Classes.objects.filter(module_holder=module_holder)
        form.fields['section'].queryset = Section.objects.filter(module_holder=module_holder)  
        form.fields['subject'].queryset = Subject.objects.filter(module_holder=module_holder)  
        return form


    def post(self, request):
        if request.user.is_staff:
            module_holder = request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=request.user.id)
            module_holder = this_holder.module_holder 

        form = StudentMarkSearchForm(module_holder, request.POST)
        
        mark_ditribution_header = MarkDistribution.objects.filter(
            module_holder=module_holder,
            subject_name=Subject.objects.get(pk=request.POST.get('subject')),
            class_name = Classes.objects.get(pk=request.POST.get('class_name')),
            ).last()
        
        collect_student_form_with_data = []
        if form.is_valid():            
            all_searched_student = Admission.objects.filter(
                admission_class = Classes.objects.get(pk=request.POST.get('class_name')),
                admission_section = Section.objects.get(pk=request.POST.get('section')),
                module_holder = module_holder
            )
         
            getting_marks = ''
            for student in all_searched_student:
                getting_marks = StudentMark.objects.filter(
                    student_name = Admission.objects.get(pk=student.pk),
                    section = Section.objects.get(pk=request.POST.get('section')),
                    class_name = Classes.objects.get(pk=request.POST.get('class_name')),
                    subject = Subject.objects.get(pk=request.POST.get('subject')),
                    module_holder = module_holder
                ).first()
            
                if getting_marks is not None:
                    collect_student_form_with_data.append({
                            'studentID': student.pk,
                            'student_name': Admission.objects.get(pk=student.pk),
                            'forms': StudentMarkForm(
                                initial={
                                        'student_name': Admission.objects.get(pk=student.pk),
                                        'section': student.admission_section,
                                        'class_name': student.admission_class,
                                        'subject': getting_marks.subject,
                                        'exam': getting_marks.exam,
                                        'attendance': getting_marks.attendance,
                                        'class_test': getting_marks.class_test,
                                        'assignment': getting_marks.assignment,
                                }
                            )
                        })
                else:
                    collect_student_form_with_data.append({
                            'studentID': student.pk,
                            'student_name': Admission.objects.get(pk=student.pk),
                            'forms': StudentMarkForm(initial={
                            'student_name': Admission.objects.get(pk=student.pk),
                            'section': student.admission_section,
                            'class_name': student.admission_class,
                            'exam': 0,
                            'attendance': 0,
                            'class_test': 0,
                            'assignment': 0,
                        })
                    })


        context = {
            'mark_ditribution_header':mark_ditribution_header,
            'collect_student_form_with_data': collect_student_form_with_data,
            'form': form,
            'class_name': request.POST.get('class_name'),
            'subjectid': request.POST.get('subject'),
        }
        return render(request, self.template_name, context)

   

class StudentMarkCreate(PermissionRequiredMixin, LoginRequiredMixin ,FormView):
    login_url = 'home:login'
    template_name= 'student/mark_search.html'  
    form_class = StudentMarkSearchForm 
    permission_required = 'student.add_studentmark'
    
    def post(self, request):
        if request.user.is_staff:
            module_holder = request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=request.user.id)
            module_holder = this_holder.module_holder
            
        mark_ditribution_header = MarkDistribution.objects.filter(
            module_holder=module_holder,
            subject_name=Subject.objects.get(pk=request.POST.get('subject')),
            class_name = Classes.objects.get(pk=request.POST.get('class_name')),
            ).last()
        index = 0
        for student in request.POST.getlist('student_name'):
            getting_marks = StudentMark.objects.filter(
                 student_name = Admission.objects.get(pk=request.POST.getlist('student_name')[index]),
                 section = Section.objects.get(pk=request.POST.get('section')),
                 class_name = Classes.objects.get(pk=request.POST.get('class_name')),
                 subject = Subject.objects.get(pk=request.POST.get('subject')),
                 module_holder = module_holder
            ).first()
            if getting_marks is not None:# IF there is  marks already  in sudent marks table. than update it
                StudentMark.objects.filter(
                        student_name = Admission.objects.get(pk=request.POST.getlist('student_name')[index]),
                        section = Section.objects.get(pk=request.POST.get('section')),
                        class_name = Classes.objects.get(pk=request.POST.get('class_name')),
                        subject = Subject.objects.get(pk=request.POST.get('subject')),
                        module_holder = module_holder
                ).update(
                        exam = request.POST.getlist('exam')[index],
                        attendance = request.POST.getlist('attendance')[index],
                        class_test = request.POST.getlist('class_test')[index],
                        assignment = request.POST.getlist('assignment')[index]
                )
                messages.add_message(
                    request, messages.SUCCESS, 'Student Marks has been updated.',
                    fail_silently=True,
                )

            else:  # IF there is not marks in sudent marks table. than sav it
               StudentMark(
                        student_name = Admission.objects.get(pk=request.POST.getlist('student_name')[index]),
                        section = Section.objects.get(pk=request.POST.get('section')),
                        class_name = Classes.objects.get(pk=request.POST.get('class_name')),
                        subject = Subject.objects.get(pk=request.POST.get('subject')),
                        exam = request.POST.getlist('exam')[index],
                        attendance = request.POST.getlist('attendance')[index],
                        class_test = request.POST.getlist('class_test')[index],
                        assignment = request.POST.getlist('assignment')[index],
                        module_holder = module_holder
               ).save()
               messages.add_message(
                    request, messages.SUCCESS, 'Student Marks has been Saved!.',
                    fail_silently=True,
                )
            index = index+1
        # new data searching will be start from here
        all_searched_student = Admission.objects.filter(
            admission_class = Classes.objects.get(pk=request.POST.get('class_name')),
            admission_section = Section.objects.get(pk=request.POST.get('section')),
            module_holder = module_holder
        )
        collect_student_form_with_data = []
        getting_marks = ''
        for student in all_searched_student:
            getting_marks = StudentMark.objects.filter(
                 student_name = Admission.objects.get(pk=student.pk),
                 section = Section.objects.get(pk=request.POST.get('section')),
                 class_name = Classes.objects.get(pk=request.POST.get('class_name')),
                 subject = Subject.objects.get(pk=request.POST.get('subject')),
                 module_holder = module_holder
            ).first()
           
            if getting_marks is not None:
                collect_student_form_with_data.append({
                        'studentID': student.pk,
                        'student_name': Admission.objects.get(pk=student.pk),
                        'forms': StudentMarkForm(initial={
                        'student_name': Admission.objects.get(pk=student.pk),
                        'section': student.admission_section,
                        'class_name': student.admission_class,
                        'subject': getting_marks.subject,
                        'exam': getting_marks.exam,
                        'attendance': getting_marks.attendance,
                        'class_test': getting_marks.class_test,
                        'assignment': getting_marks.assignment,

                    })
                }
                )
            else:
                collect_student_form_with_data.append({
                    'studentID': student.pk,
                    'student_name': Admission.objects.get(pk=student.pk),
                    'forms': StudentMarkForm(initial={
                        'student_name': student.pk,
                        'section': student.admission_section,
                        'class_name': student.admission_class,
                        'exam': 0,
                        'attendance': 0,
                        'class_test': 0,
                        'assignment': 0,
                    })
                }
                )


        context = {
            'mark_ditribution_header': mark_ditribution_header,
            'collect_student_form_with_data': collect_student_form_with_data,
            'form': StudentMarkSearchForm(module_holder, request.POST),
            'class_name': request.POST.get('class_name'),
            'subjectid': request.POST.get('subject')
        }
        return render(request, self.template_name, context)

    # def get_form(self, **kwargs):
    #     form = super(StudentMarkSearch, self).get_form(**kwargs)
    #     form['StudentMarkSearchForm'] = StudentMarkSearchForm()
    #     return form

# START WORKING ON MARKS DIETRIBUTION

class MarkDistributionCreate(LoginRequiredMixin, SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    '''Assigning marks'''
    model = MarkDistribution
    fields = ['class_name','subject_name','exam','attendance','class_test','assignment']
    context_object_name = 'markdist'
    template_name = 'student/mark_distribution.html'
    permission_required = 'student.add_markdistribution' 
    login_url = 'home:login'
    success_message = 'Mark Distribution has been saved!'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        form.instance.module_holder = module_holder
        if self.model.objects.filter(module_holder=module_holder,subject_name=self.request.POST.get('subject_name'), class_name=self.request.POST.get('class_name')):
            messages.warning(self.request,'Data already Exists. Please update or create new one')
            return redirect("student:mark_distribution_create")
        else:
            return super().form_valid(form)

    def get_form(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
            
        form = super(MarkDistributionCreate, self).get_form(**kwargs)
        form.fields['class_name'].widget.attrs = {'class': 'basic-multiple'}
        form.fields['subject_name'].widget.attrs = {'class': 'basic-multiple'}
        form.fields['class_name'].queryset = Classes.objects.filter(module_holder=module_holder)
        form.fields['subject_name'].queryset = Subject.objects.filter(module_holder=module_holder)
        return form

    def get_context_data(self, **kwargs):
        context = super(MarkDistributionCreate, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
            
        context['markdist'] = MarkDistribution.objects.filter(module_holder=module_holder)
        return context


class MarkDistributionUpdate(PermissionRequiredMixin,SuccessMessageMixin, LoginRequiredMixin ,UpdateView):
    model = MarkDistribution
    fields = ['class_name','subject_name','exam','attendance','class_test','assignment']
    login_url = 'home:login'
    context_object_name = 'markdist'
    template_name = 'student/mark_distribution.html'
    permission_required = 'student.change_markdistribution' 
    success_message = 'Mark Distribution has been updated!'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
            
        form.instance.module_holder = module_holder
        return super().form_valid(form)

    def get_form(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
            
        form = super(MarkDistributionUpdate, self).get_form(**kwargs)
        form.fields['class_name'].widget.attrs = {'class': 'basic-multiple'}
        form.fields['subject_name'].widget.attrs = {'class': 'basic-multiple'}
        form.fields['class_name'].queryset = Classes.objects.filter(module_holder=module_holder)
        form.fields['subject_name'].queryset = Subject.objects.filter(module_holder=module_holder)
        return form

    def get_context_data(self, **kwargs):
        context = super(MarkDistributionUpdate, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
            
        context['markdist'] = MarkDistribution.objects.filter(module_holder=module_holder)
        return context


class MarkDistributionDelete(PermissionRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    login_url = 'home:login'
    permission_required = 'student.delete_markdistribution' 
    success_message = 'Mark Distribution has been deleted!'
    model = MarkDistribution
    success_url = reverse_lazy('student:mark_distribution_create')


# ADMISSION CLASSES START HERE
class AdmissionCreate(PermissionRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = 'home:login'
    model = Admission    
    template_name = 'student/admission.html'
    permission_required = 'student.add_admission' 
    success_message = 'Admission has been Created!'
    form_class = AdmissionForm
    # success_url = '/student/admission/view/'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        
        # password = make_password(form.instance.password)
        # form.instance.password = password
        form.instance.module_holder = module_holder
        return super().form_valid(form)

    def form_invalid(self, form):
        password = make_password(form.instance.password)
        form.instance.password = password
        print('================1============', form.instance.password)
       
        print('================2============', form.instance.password)

        return super().form_invalid(form)
    # def post(self, request,  *args, **kwargs):
    #     return CreateView(request, *args, **kwargs)
    #     # form = self.get_form()
    #     # self.object = self.get_object()
    #     # if form.is_valid():
    #     #     return self.form_valid(form)
    #     # else:
    #     #     return self.form_invalid(form)
        
        

    def get_form(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
            
        last_id = Admission.objects.filter(module_holder=module_holder).first()
        # print('last ID==================',last_id.admission_registration)
        if last_id is None:
            last_id = '0'
        else:
            last_id = last_id.admission_registration

        form = super(AdmissionCreate, self).get_form(**kwargs)
        # form.fields['gender'].widget = forms.RadioSelect()
        form.fields['admission_registration'].widget = forms.TextInput(attrs={'value': generate_reg(last_id), 'readonly': 'readonly'})
        # form.fields['free_student'].widget = forms.RadioSelect()
        form.fields['admission_date'].widget = forms.TextInput(attrs = {'type': 'date','value':timezone.now().strftime('%Y-%m-%d')})
        form.fields['date_of_birth'].widget = forms.TextInput(attrs = {'type': 'date'})
        form.fields['cast'] = forms.CharField(required=False)
        form.fields['photo'] = forms.ImageField(required=False)
        form.fields['annual_fund'] = forms.CharField(required=False)
        form.fields['admission_class'].queryset = Classes.objects.filter(module_holder=module_holder)
        form.fields['admission_section'].queryset = Section.objects.filter(module_holder=module_holder)        
        form.fields['admission_class'].widget.attrs = {'class': 'basic-multiple'}
        form.fields['admission_section'].widget.attrs = {'class': 'basic-multiple'}
        # form.fields['photo'].widget = forms.TextInput(attrs={'type': 'file', 'class': 'custom-input-file custom-input-file--2'})
        return form

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
      
        context = super(AdmissionCreate, self).get_context_data(**kwargs)
    
        context['classesform'] = ClassesForm(module_holder)
        context['sectionform']  = SectionForm()
        context['admissioncreateurl'] = '/student/admission/create/'
        return context

class AdmissionUpdate(PermissionRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    login_url = 'home:login'
    model = Admission
    fields = admissionfields
    template_name = 'student/admission.html'
    permission_required = 'student.change_admission' 
    success_message = 'Student data has been updated!'
    # success_url = '/student/admission/view/'
    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
            
        form.instance.module_holder = module_holder
        return super().form_valid(form)

    def get_form(self, **kwargs):
        form = super(AdmissionUpdate, self).get_form(**kwargs)
        form.fields['gender'].widget = forms.RadioSelect()
        form.fields['admission_registration'].widget = forms.TextInput({'readonly': 'readonly'})
        form.fields['free_student'].widget = forms.RadioSelect()
        form.fields['admission_date'].widget = forms.TextInput(attrs = {'type': 'date','value':timezone.now().strftime('%Y-%m-%d')})
        form.fields['date_of_birth'].widget = forms.TextInput(attrs = {'class': 'date'})
        form.fields['cast'] = forms.CharField(required=False)
        form.fields['photo'] = forms.ImageField(required=False)
        form.fields['annual_fund'] = forms.CharField(required=False)
        form.fields['admission_section'].widget.attrs={'class': 'basic-multiple'}
        form.fields['admission_class'].widget.attrs['class']='basic-multiple'
        form.fields['admission_class'].queryset = Classes.objects.filter(module_holder=self.request.user)
        form.fields['admission_section'].queryset = Section.objects.filter(module_holder=self.request.user)
        form.fields['admission_class'].widget.attrs = {'class': 'basic-multiple'}
        form.fields['admission_section'].widget.attrs = {'class': 'basic-multiple'}
        return form

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
      
        context = super(AdmissionUpdate, self).get_context_data(**kwargs)    
        context['classesform'] = ClassesForm(module_holder)
        context['sectionform']  = SectionForm()
        context['admissioncreateurl'] = '/student/student/admission/view/'+str(self.kwargs.get('pk'))+'/update'
        return context

class AdmissionDetail(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    login_url = 'home:login'
    model = Admission
    template_name = 'student/admission_detail.html'
    context_object_name = 'admisssion_details'
    permission_required = 'student.view_admission' 

    def get_context_data(self, **kwargs):
        context = super(AdmissionDetail, self).get_context_data(**kwargs)
        return context


class AdmissionView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    login_url = 'home:login'
    model = Admission
    template_name = 'student/admission_view.html'
    permission_required = 'student.view_admission' 

    def get_context_data(self, **kwargs):
        context = super(AdmissionView, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
            
        context['admission_view'] = Admission.objects.filter(module_holder=module_holder)
        return context


class AdmissionDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = 'home:login'
    permission_required = 'student.delete_admission' 
    model = Admission
    success_url = reverse_lazy('student:admission_view')

    


# INDVIGUAL STUDENT 
class IndividualMarksView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    login_url = 'home:login'
    permission_required = 'student.view_markdistribution' 
    days = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
    ]
    
    slug_url_kwargs = 'year_slug'
    fee_year = timezone.now().strftime('%Y')
    tab = False
    # def get_object(self, queryset=None):
    #     return queryset.get(slug=self.slug)

    def get(self, request, *args, **kwargs):
        # admission = get_object_or_404(Admission, pk=kwargs['pk'])
        # global fee_year
        print(request.GET)
        if request.GET.get('year') and request.GET.get('tab'):
            self.fee_year = request.GET.get('year')
            self.tab = True

        student_id = kwargs['student_name']
        admission = Admission.objects.get(pk=kwargs['student_name'])
        routines = []      
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        for day in self.days:
            matched_routine = Routine.objects.filter(module_holder=module_holder, class_name=admission.admission_class, school_day__contains=[day])
            routines.append(
                {
                    'days':day,
                    'routine': matched_routine
                }
            )
        student_attendance_detail_year  = []  
        monthly_detal = [] 
        daily_detail = []
        total_holidays = 0
        total_leave = 0
        total_present = 0
        total_late = 0
        total_absent = 0  
        total_off = 0   
           
        for year in range(start_year, int(current_year)+1):
            # monthly_detal.clear()
            for month in all_months:
                # daily_detail.clear()
                for day in range(1, monthrange(year,int(month))[1]+1):
                    if day < 10:
                        day = '0'+str(day)
                    
                    date = str(year)+'-'+str(month)+'-'+str(day)
                    date = datetime.datetime.strptime(date,'%Y-%m-%d')
                    daily = Attendance.objects.filter(student_id=admission, date=date)
                    daily_inner = []
                    if daily.exists():
                        for detail in daily:
                            if attendance_converter(detail.attendance_selection, date) == 'P':
                                total_present +=1
                            elif attendance_converter(detail.attendance_selection, date) == 'A':
                                total_absent +=1
                            elif attendance_converter(detail.attendance_selection, date) == 'O':
                                total_off +=1
                            elif attendance_converter(detail.attendance_selection, date) == 'H':
                                total_holidays +=1
                            elif attendance_converter(detail.attendance_selection, date) == 'L':
                                total_leave +=1
                            elif attendance_converter(detail.attendance_selection, date) == 'L-I':
                                total_late +=1
                            
                            # print('------------------------------')
                            # print(day)

                            daily_inner.append({
                                'day': day,
                                'month': convert_month_into_string(month),
                                'attendance': attendance_converter(detail.attendance_selection, date),
                                'remark': detail.remarks,
                                'att_date': detail.date
                            })
                    else:
                        if attendance_converter('', date) == 'P':
                            total_present +=1
                        elif attendance_converter('', date) == 'A':
                            total_absent +=1
                        elif attendance_converter('', date) == 'O':
                            total_off +=1
                        elif attendance_converter('', date) == 'H':
                            total_holidays +=1
                        elif attendance_converter('', date) == 'L':
                            total_leave +=1
                        elif attendance_converter('', date) == 'L-I':
                            total_late +=1
                            
                        # print('------------------------------')
                        # print(day)
                        daily_inner.append({
                                'day': day,
                                'month': convert_month_into_string(month),
                                'attendance': attendance_converter('', date),
                                'remark': 'N/A',
                                'att_date': 'N/A'
                        })
                    # daily_detail.append(daily_inner)
                    monthly_detal.append(
                        {'daily': daily_inner}
                    )
            student_attendance_detail_year.append({
                'year': year,
                'month': monthly_detal
            })
            
            # routine.append()
            collect_std_marks_subs = []
            student_object = Admission.objects.filter(pk=student_id).first()
            class_of_student = Classes.objects.filter(class_name=student_object.admission_class.class_name, module_holder=module_holder).first()
            subjects = Subject.objects.filter(class_name__contains=class_of_student.pk, module_holder=module_holder)            
            get_calculated_marks = []
            for mos in subjects:
                out_of_marks = MarkDistribution.objects.filter(subject_name=mos.pk).first()
                in_of_marks = StudentMark.objects.filter(class_name=class_of_student.pk, subject=mos.pk, student_name=student_id,module_holder=module_holder).first()
                # marks_of_student = StudentMark.objects.filter(student_name=student_id, module_holder=module_holder)
                exam = 0
                attendance = 0
                assignment = 0
                class_test = 0

                calculated_marks_object = CalculateResults.objects.filter(student=admission, module_holder=module_holder, subject=mos.pk)
                for calc in calculated_marks_object:
                    get_calculated_marks.append({
                        'exam_type': calc.exam_type,
                        'total_marks': calc.total_marks,
                        'assigned_marks': calc.marks,
                        'subject': calc.subject

                    })
                if out_of_marks:
                    in_of_marks = StudentMark.objects.filter(class_name=class_of_student.pk, subject=mos.pk, student_name=student_id,module_holder=module_holder).first()

                    if in_of_marks:
                        exam = in_of_marks.exam
                        attendance = in_of_marks.attendance
                        assignment = in_of_marks.assignment
                        class_test = in_of_marks.class_test

                    collect_std_marks_subs.append({
                    'subject_name': mos.subject_name,
                    'examout': out_of_marks.exam,
                    'attendanceout': out_of_marks.attendance,
                    'assignmentout': out_of_marks.assignment,
                    'classtestout': out_of_marks.class_test,
                    'examin': exam,
                    'attendancin': attendance,
                    'assignmentin': assignment,
                    'classtestin': class_test


                })
                else:
                    collect_std_marks_subs.append({
                    'subject_name': mos.subject_name,
                    'examout': 0,
                    'attendanceout': 0,
                    'assignmentout': 0,
                    'classtestout': 0,
                    'examin': exam,
                    'attendancin': attendance,
                    'assignmentin': assignment,
                    'classtestin': class_test


                })
            # print(collect_std_marks_subs)
            # print('mamamamamam',subjects)

            # START WORKING WITH STUDENT PAYMENT SYSTEM
        class_object = Classes.objects.filter(class_name__contains=admission.admission_class.class_name).first()
        voucher_object = Voucher.objects.filter(student_name=student_id)
        
        payment_system = []
        for voucher in voucher_object:
            payment_system.append({
                'fee_month': voucher.fee_month,
                'tution_fee_payable': voucher.monthly_tution_fee,
                'tution_fee_paid': voucher.monthly_tution_fee_paid
            })
        payment_system_info = {
            'admission_date': admission.admission_date,
            'monthly_fee': class_object.fee,
           
        }    

        context = {
            'collect_std_marks_subs': collect_std_marks_subs,
            'routines': routines,
            'admission': admission,
            'student_attendance_detail_year':student_attendance_detail_year,
            'total_present': total_present,
            'total_absent': total_absent,
            'total_off': total_off,
            'total_holidays': total_holidays,
            'total_leave': total_leave,
            'total_late': total_late,
            'payment_system_info': calculate_student_fee_for_year(request, student_id, admission, self.fee_year),
            'get_calculated_marks': get_calculated_marks,
            'tab': self.tab,
            'range': range(2015,2030),
        }
        return render(request, 'attendance/individual_marks_view.html', context)
        

def calculate_student_fee_for_year(request, *args, **kwargs):
    class_object = Classes.objects.filter(class_name__contains=args[1].admission_class.class_name).first()
    
    admission_month = int(str(args[1].admission_date).split('-')[1])
    payment_system = []
    total_payable = 0
    total_paid = 0
    for month in range(admission_month, 13):
        voucher_object = Voucher.objects.filter(student_name=args[0], month=add_zero_to_month(month), year=args[2])
        total_payable = total_payable+args[1].monthly_tution_fee
        # total_paid = total_paid+total_payable
        
        if voucher_object:
            
            for voucher in voucher_object:
                # total_payable = total_payable+voucher.monthly_tution_fee
                if voucher.monthly_tution_fee != args[1].monthly_tution_fee:
                    detected = args[1].monthly_tution_fee-voucher.monthly_tution_fee 
                    total_payable = total_payable-detected
                total_paid = total_paid+voucher.monthly_tution_fee_paid
                payment_system.append({
                    'status': 'Voucher Generated',
                    'fee_month': str(args[2])+'-'+convert_month_2_string(int(str(voucher.fee_month).split('-')[1])),
                    'tution_fee_payable': voucher.monthly_tution_fee,
                    'tution_fee_paid': voucher.monthly_tution_fee_paid,
                    'total_payable': total_payable,
                    'total_paid': total_paid
                })
        else:
            payment_system.append({
                    'status': 'Voucher Not Generated',
                    'fee_month': str(args[2])+'-'+convert_month_2_string(month),
                    'tution_fee_payable': args[1].monthly_tution_fee,
                    'tution_fee_paid': 0,
                    'total_payable': total_payable,
                    'total_paid': total_paid

                })
    
    print('sdasdadsadasdasda', args)
    payment_system_info = {
        'admission_date': args[1].admission_date,
        'monthly_fee': class_object.fee,
    }   
    context = {
        'payment_system_info': payment_system_info,
        'payment_system': payment_system
    }
    return context 

def add_zero_to_month(month):
    if len(str(month))<2:
        return '0'+str(month)
    else:
        return str(month)

# SECTION START HERE
class SectionCreate(PermissionRequiredMixin, SuccessMessageMixin, LoginRequiredMixin ,CreateView):
    login_url = 'home:login'
    template_name = 'student/section_view_or_create.html'
    model = Section
    fields = ['section_name']
    permission_required = 'student.add_section'
    success_message = 'Section has been Created!'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
            
        form.instance.module_holder = module_holder
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SectionCreate, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
            
        context['section'] = Section.objects.filter(module_holder=module_holder)
        return context


class SectionUpdate(PermissionRequiredMixin, SuccessMessageMixin, LoginRequiredMixin ,UpdateView):
    login_url = 'home:login'
    template_name = 'student/section_view_or_create.html'
    model = Section
    fields = ['section_name']
    permission_required = 'student.change_section'
    success_message = 'Section has been Updated!'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
            
        form.instance.module_holder = module_holder
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SectionUpdate, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
            
        context['section'] = Section.objects.filter(module_holder=module_holder)
        return context


class SectionDelete(PermissionRequiredMixin, LoginRequiredMixin ,DeleteView):
    login_url = 'home:login'
    permission_required = 'student.delete_section'
    model = Section
    success_url = reverse_lazy('student:create_section')

# SECTION START HERE
class ExamsView(SuccessMessageMixin, LoginRequiredMixin, TemplateView):
    login_url = 'home:login'
    template_name = 'student/exams.html'
    model = Exams
    # permission_required = 'student.add_section'

    def get_context_data(self, **kwargs):
        context = super(ExamsView, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
            
        context['exams'] = Exams.objects.filter(module_holder=module_holder)
        return context

class ExamsDetail(LoginRequiredMixin, DetailView):
    login_url = 'home:login'
    model = Exams
    template_name = 'student/exams_detail_view.html'
    context_object_name = 'exams_detail'
    # permission_required = 'student.view_admission' 

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        
        getting_students = Admission.objects.filter(module_holder=module_holder, admission_class=self.object.class_name.pk)
       
        students_list = []
        for student in getting_students:
            status = 'not-sent'
            exists_student = ExamEmail.objects.filter(student__contains=[str(student.pk)], module_holder=module_holder,subject=self.object.subject_name, exam=self.object.pk )
            if exists_student:
                status = 'sent'
            else:
                status = 'not-sent'
            students_list.append({
                'photo': student.photo,
                'name_of_student': student.name_of_student,
                'admission_registration': student.admission_registration,
                'Student_email_address': student.Student_email_address,
                'father_email_address': student.father_email_address,
                'contact': student.contact,
                'pk': student.pk,
                'status': status
            })
        context = super(ExamsDetail, self).get_context_data(**kwargs)
        context['schoolprofile'] = SchoolProfile.objects.get(module_holder=module_holder)
        context['students'] = students_list
        context['module_holder'] = module_holder
        context['subject'] = self.object.subject_name

        return context

def get_class_asignments(request, pk, class_name, subject):
    if request.user.is_staff:
        module_holder = request.user.username
    else:
        this_holder = Teacher.objects.get(user_ptr_id=request.user.id)
        module_holder = this_holder.module_holder

    if request.method=='POST':
        index = 0        
        for data in request.POST.getlist('marks'):
            marks = ''
            exam_type = ''
            marks = request.POST.getlist('marks')[index]
            exam_type = request.POST.getlist('exam_type')[index]
            form_form_update_exists = CalculateResults.objects.filter(
                student=Admission.objects.get(pk=request.POST.get('student_id')),
                class_name=Classes.objects.get(pk=request.POST.get('class_name')),
                subject=Subject.objects.get(pk=request.POST.get('subject')),
                exam=ExamEmail.objects.get(pk=request.POST.getlist('exam_id')[index]),
                exam_type=exam_type,
                module_holder=request.POST.get('module_holder')
            )
            form = CalculateResults(
                student=Admission.objects.get(pk=request.POST.get('student_id')),
                class_name=Classes.objects.get(pk=request.POST.get('class_name')),
                subject=Subject.objects.get(pk=request.POST.get('subject')),
                exam=ExamEmail.objects.get(pk=request.POST.getlist('exam_id')[index]),
                total_marks=request.POST.getlist('total_marks')[index],
                marks=marks,
                exam_type=exam_type,
                module_holder=request.POST.get('module_holder')
            )
            if form_form_update_exists:
                messages.success(request,'Data has been updated, kindly close this window for further process.')
                form_form_update_exists.update(marks=marks)
            else:
                form.save()
                messages.success(request,'Data has been Saved, kindly close this window for further process.')
            index = index+1

         
        
    exam_type =[]
    types = list(['midterm','final','classtest','assignment'])
    mark_distribution = MarkDistribution.objects.get(class_name=Classes.objects.get(pk=class_name))
    
    
    total_section_mark = 0
    for typ in types:
        # exam_detail.clear()  
        exam_detail = []
        
        marks_assign_for_next_time = 'undeclared'
        examsent = ExamEmail.objects.filter(student__contains=[str(pk)])
        for examesend in examsent:
            calculate_result = CalculateResults.objects.filter(module_holder=module_holder, student=pk, class_name=class_name,subject=subject, exam=examesend.pk).first()
            if calculate_result:
                marks_assign_for_next_time = calculate_result.marks
            else:
                marks_assign_for_next_time = 'undeclared'
              
            exam = Exams.objects.filter(exams_name=examesend.exam, exam_type=typ, subject_name=subject).first()
            if exam:
                exam_detail.append(
                {
                    'exam_name': exam.exams_name,
                    'total_mark': exam.marks,
                    'exam_type': exam.exam_type,
                    'examsendpk': examesend.pk,
                    'calculate_result': calculate_result,
                    'marks_assign_for_next_time': marks_assign_for_next_time
                    
                })        
        exam_type.append({'type': typ, 'details':exam_detail, 'total_section_mark':total_section_mark })
        
    

    return render(request, 
    'student/get_class_asignments.html',
    {'exam_type': exam_type,
     'mark_distribution': mark_distribution,
     'exam_id': pk,
     'subject': subject,
     'subject_name': Subject.objects.get(pk=subject),
     'student_id': pk,
     'class_id':class_name,
     'module_holder': module_holder
     })

def getting_marks_from_calculated(request):
    if request.user.is_staff:
        module_holder = request.user.username
    else:
        this_holder = Teacher.objects.get(user_ptr_id=request.user.id)
        module_holder = this_holder.module_holder

    exam_type = request.GET.get('exam_type')
    student_id = request.GET.get('student_id')
    class_name = request.GET.get('class_name')
    subject_id = request.GET.get('subject_id')
    total_head_marks = request.GET.get('total_head_marks')
    exams = ''
    if exam_type == 'midterm':
        exams = list(['midterm','final'])
    else:
        exams = list([exam_type])
    
    exam_data = CalculateResults.objects.filter(
        student = Admission.objects.get(pk=student_id),
        class_name = Classes.objects.get(pk=class_name),
        subject=subject_id,
        module_holder=module_holder,
        exam_type__in=exams
    )
    print()
    # print(exam_data)
    total_required = list()
    total_assigned = list()
    if exam_data:
        for ed in exam_data:
            if ed.marks == 'undeclared':
                marks = 0
            else:
                marks = ed.marks
            total_required.append(ed.total_marks)
            total_assigned.append(int(marks))
        result = (sum(total_assigned)/sum(total_required)) * int(total_head_marks)
    else:
        result = 0

    # print('result', result)

    
    return JsonResponse({'data':result})

def SendEmail_SaveData(request):
    if request.user.is_staff:
        module_holder = request.user.username
    else:
        this_holder = Teacher.objects.get(user_ptr_id=request.user.id)
        module_holder = this_holder.module_holder

    if request.method=='POST':
        examemail = ExamEmail(
            module_holder=request.POST.get('module_holder'),
            exam=Exams.objects.get(exams_name=request.POST.get('exam')), 
            subject=Subject.objects.get(subject_name=request.POST.get('subject'), module_holder=module_holder), 
            student=request.POST.getlist('pk')
        )
        if request.POST.getlist('pk') == []:
            messages.warning(request,"Please Select at leaset one Student!")
            return redirect('student:detail_exams', pk=Exams.objects.get(exams_name=request.POST.get('exam')).pk)
        else:
            check = ExamEmail.objects.filter(exam=Exams.objects.get(exams_name=request.POST.get('exam')))
            if check:
                check.update(module_holder=request.POST.get('module_holder'),
                    exam=Exams.objects.get(exams_name=request.POST.get('exam')), 
                    student=request.POST.getlist('pk'))
            else:
                examemail.save()
        messages.success(request,"Email has been sent to all selected student. check status!")
        return redirect('student:detail_exams', pk=Exams.objects.get(exams_name=request.POST.get('exam')).pk)
    
    
class SendEmailForExam(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = 'home:login'
    template_name = 'student/exams_create.html'
    model = ExamEmail
    fields = [
        'exam',
        'student',
    ]
    permission_required = 'student.add_section'
    success_message = 'Email has been sent to all selected students!'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
            
        form.instance.module_holder = module_holder
        return super().form_valid(form) 

# SECTION START HERE
class ExamsCreate(SuccessMessageMixin, LoginRequiredMixin ,CreateView):
    login_url = 'home:login'
    template_name = 'student/exams_create.html'
    model = Exams
    fields = [
        'exams_name',
        'class_name',
        'subject_name',
        'exam_type',
        'marks',
        'exam_detail_file',
        'open_date',
        'due_date',
        'remarks'
    ]
    success_url = '/student/viewexams/view'
    # permission_required = 'student.add_section'
    success_message = 'Exam has been Created!'
    
    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
            
        form.instance.module_holder = module_holder
        return super().form_valid(form)
        
    def get_form(self, **kwargs):        
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        form = super(ExamsCreate, self).get_form(**kwargs) 
        form.fields['open_date'].widget = forms.TextInput(attrs={'type': 'date', 'value': timezone.now().strftime('%Y-%m-%d')})
        form.fields['due_date'].widget = forms.TextInput(attrs={'type': 'date', 'value': timezone.now().strftime('%Y-%m-%d')})
        form.fields['exam_type'].widget.attrs={'class': 'basic-multiple'}
        form.fields['class_name'].widget.attrs={'class': 'basic-multiple'}
        form.fields['subject_name'].widget.attrs['class']='basic-multiple'
        form.fields['class_name'].queryset = Classes.objects.filter(module_holder=module_holder)
        form.fields['subject_name'].queryset = Subject.objects.filter(module_holder=module_holder)
        return form
    
    def get_context_data(self, **kwargs):
        context = super(ExamsCreate, self).get_context_data(**kwargs)
        context['examcreateurl'] = '/student/createexams/'
        return context

class ExamsUpdate(SuccessMessageMixin, LoginRequiredMixin ,UpdateView):
    login_url = 'home:login'
    template_name = 'student/exams_create.html'
    model = Exams
    fields = [
        'exams_name',
        'class_name',
        'subject_name',
        'exam_type',
        'marks',
        'exam_detail_file',
        'open_date',
        'due_date',
        'remarks'
    ]
    # permission_required = 'student.change_section'
    success_message = 'Exam has been Updated!'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
            
        form.instance.module_holder = module_holder
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ExamsUpdate, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
            
        context['exams'] = Exams.objects.filter(module_holder=module_holder)
        context['examcreateurl'] = '/student/updateexams/'+str(self.kwargs.get('pk'))+'/edit'
        return context
    

        


class ExamsDelete(PermissionRequiredMixin, LoginRequiredMixin ,DeleteView):
    login_url = 'home:login'
    permission_required = 'student.delete_section'
    model = Exams
    success_url = reverse_lazy('student:view_exams')


# SECTION ENDS HERE
class AttendanceView(PermissionRequiredMixin, LoginRequiredMixin ,CreateView):
    login_url = 'home:login'
   
    
    template_name = 'attendance/attendane_view.html'
    permission_required = 'student.view_attendance'

    

    # def get_form(self, **kwargs):
        # if self.request.user.is_staff:
        #     module_holder = self.request.user.username
        # else:
        #     this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
        #     module_holder = this_holder.module_holder
            
    #     form = super(AttendanceView, self).get_form(**kwargs)
    #     form.fields['section'].widget.attrs={'class': 'basic-multiple'}
    #     form.fields['section'].queryset = Section.objects.filter(module_holder=module_holder)
    #     form.fields['classes'].widget.attrs['class']='basic-multiple'
    #     form.fields['classes'].queryset = Classes.objects.filter(module_holder=module_holder)
    #     return form

    def get(self, request):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form = AttendanceForm(module_holder)
        return render(request, self.template_name, {'form': form})
        
    get_attendance = []   
    def post(self, request):
        section = request.POST.get('section', 0)
        classes = request.POST.get('classes', 0)
        from_date = request.POST.get('from_date', 0)
        to_date = request.POST.get('to_date', 0)
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        
        # self.get_attendance = Attendance.objects.order_by('student_id').filter(classes=classes, section=section, current_month=current_month)
        if from_date and to_date and classes:
            self.get_attendance = Attendance.objects.filter(module_holder=module_holder, date__range=[from_date, to_date], classes=classes)

        elif from_date and to_date and section:
            self.get_attendance = Attendance.objects.filter(module_holder=module_holder, date__range=[from_date, to_date], section=section)
        
        elif classes and section:
            self.get_attendance = Attendance.objects.filter(module_holder=module_holder, current_month=current_month, classes=classes, section=section)
            
        elif not classes and section:
            self.get_attendance = Attendance.objects.filter(module_holder=module_holder, current_month=current_month, section=section)
        
        elif not Section and classes:
            self.get_attendance = Attendance.objects.filter(module_holder=module_holder, current_month=current_month, classes=classes)

        elif from_date and to_date:
            self.get_attendance = Attendance.objects.filter(module_holder=module_holder, date__range=[from_date, to_date])
        else:
            self.get_attendance = Attendance.objects.filter(module_holder=module_holder, date__range=[timezone.datetime.now().strftime('%m-%d-%Y'), to_date])

        student_name = []
        for get_attend in self.get_attendance:
            if get_attend.student_id not in student_name:
                student_name.append(get_attend.student_id)

        student_attendance_detail  = []    
        for student_id in student_name:
            present = Attendance.objects.filter(module_holder=module_holder, student_id=student_id, current_month=current_month, attendance_selection=1).count()
            absent = Attendance.objects.filter(module_holder=module_holder, student_id=student_id, current_month=current_month, attendance_selection=2).count()
            leave = Attendance.objects.filter(module_holder=module_holder, student_id=student_id, current_month=current_month, attendance_selection=3).count()
            latein = Attendance.objects.filter(module_holder=module_holder, student_id=student_id, current_month=current_month, attendance_selection=4).count()
            off_by_school = Attendance.objects.filter(module_holder=module_holder, student_id=student_id, current_month=current_month, attendance_selection=5).count()
            
            student_attendance_detail.append({
                'student_id': student_id,
                'present': present,
                'absent': absent,
                'leave': leave,
                'latein': latein,
                'off_by_school': off_by_school
            })
        


        # setting_data = []
        # for att in self.get_attendance:
        #     setting_data.append({
        #         'date': att.date,
        #         'registration': att.registration,
        #         'student_id': att.student_id,
        #         'attendance_selection': att.attendance_selection,
        #         'remarks': att.remarks,
        #     })

        form = AttendanceForm(module_holder, request.POST)
        
        context = {
            'get_attendance_searched': student_attendance_detail,
            'attendance_date':'date',
            'form': form
        }
        return render(request, self.template_name, context)




class AttendanceSearch(PermissionRequiredMixin, LoginRequiredMixin ,CreateView):
    login_url = 'home:login'
    model = Attendance
    fields = ['date', 'section', 'classes']
    template_name = 'attendance/attendance_search_mark.html'
    permission_required = 'student.view_attendance'

    def get_form(self, **kwargs):        
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        form = super(AttendanceSearch, self).get_form(**kwargs) 
        form.fields['date'].widget = forms.TextInput(attrs={'class': 'date', 'value': timezone.now().strftime('%Y-%m-%d')})
        form.fields['section'].widget.attrs={'class': 'basic-multiple'}
        form.fields['classes'].widget.attrs['class']='basic-multiple'
        form.fields['section'].queryset = Section.objects.filter(module_holder=module_holder)
        form.fields['classes'].queryset = Classes.objects.filter(module_holder=module_holder)
        return form

    def post(self, request):
        section = request.POST.get('section')
        classes = request.POST.get('classes')
        date = request.POST.get('date')
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        form = AttendanceForm(module_holder)
        searched_stdents = Admission.objects.filter(module_holder=module_holder, admission_section=section, admission_class=classes)
        set_student_with_attendance = []
        
        for student in searched_stdents:
            d = Attendance.objects.values('attendance_selection','remarks','subjects').filter(module_holder=module_holder, student_id=student.pk, section=student.admission_section, classes=student.admission_class, date=date )
            
            handling_subjects = []
            subjects_object = Subject.objects.filter(module_holder=module_holder, class_name__contains=student.admission_class.pk)
            if d.exists():                
                for sub in subjects_object:
                    if str(sub.pk) in str(d[0]['subjects']):
                        checked='checked="checked"'
                    else:
                        checked=''
                    handling_subjects.append({
                        'subject_name':sub.subject_name,
                        'pk': sub.pk,
                        'check': checked
                    })
                # print('===========================', d[0]['attendance_selection'])
                set_student_with_attendance.append(
                    {
                                'registration': student.admission_registration,
                                'date': date,
                                'section': section,
                                'classes': Classes.objects.filter(pk=classes).first(),
                                'student_id': Admission.objects.get(pk=student.pk),
                                'subject': [sub.subject_name for sub in Subject.objects.filter(module_holder=module_holder, class_name=student.admission_class)],
                                # Data with form if morked before                        
                                'forms_details': AttendanceForm(
                                module_holder,
                                initial={
                                'registration': student.admission_registration,
                                'date': date,
                                'section': section,
                                'classes': classes,
                                'subjects': [sub.subject_name for sub in Subject.objects.filter(module_holder=module_holder, class_name=student.admission_class)],
                                'student_id': Admission.objects.get(pk=student.pk),
                                'attendance_selection': d[0]['attendance_selection'],
                                 'remarks': d[0]['remarks']
                                }
                            ),
                        'status': 'Marked',
                        'subjects': handling_subjects
                    }
                )
            else:
                for sub in subjects_object:
                    checked='checked="checked"'
                    handling_subjects.append({
                        'subject_name':sub.subject_name,
                        'pk': sub.pk,
                        'check': checked
                    })
                set_student_with_attendance.append(
                    {
                                'registration': student.admission_registration,
                                'date': date,
                                'section': section,
                                'classes': Classes.objects.filter(pk=classes).first(),
                                'student_id': Admission.objects.get(pk=student.pk),
                                'subject': [sub.subject_name for sub in Subject.objects.filter(module_holder=module_holder, class_name=student.admission_class)],
                                # Data with form if not morked before
                                'forms_details': AttendanceForm(
                                module_holder,
                                initial={
                                'registration': student.admission_registration,
                                'date': date,
                                'section': section,
                                'classes': classes,
                                'subjects': [sub.subject_name for sub in Subject.objects.filter(module_holder=module_holder, class_name=student.admission_class)],
                                'student_id': Admission.objects.get(pk=student.pk)
                                }
                            ),
                        'status': 'Not Marked',
                        'subjects': handling_subjects
                    }
                )

        context = {
            'set_student_with_attendance': set_student_with_attendance,
            'attendance_date':date,
            'form': self.get_form
        }
        return render(request, 'attendance/attendance_search_mark.html', context)
      


class AttendanceMark(PermissionRequiredMixin, LoginRequiredMixin ,CreateView):
    login_url = 'home:login'
    model = Attendance
    fields = '__all__'
    template_name = 'attendance/attendance_search_mark.html'
    permission_required = 'student.add_attendance'

    def get_form(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
            
        form = super(AttendanceMark, self).get_form(**kwargs)
        form.fields['date'].widget = forms.TextInput(attrs={'class': 'date'})
        form.fields['section'].widget.attrs={'class': 'basic-multiple'}
        form.fields['classes'].widget.attrs['class']='basic-multiple'
        form.fields['section'].queryset = Section.objects.filter(module_holder=module_holder)
        form.fields['classes'].queryset = Classes.objects.filter(module_holder=module_holder)
        return form

    def post(self, request):
        section = request.POST.get('section')
        classes = request.POST.get('classes')
        date = request.POST.get('date')
        
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
           
        index = 0
        subjects_set = []
        for attend_rows in request.POST.getlist('registration'):
            # print(request.POST.getlist('student_id')[index])
            selected = Attendance.objects.values('attendance_selection','remarks').filter(module_holder=module_holder, student_id=request.POST.getlist('student_id')[index], section=request.POST.getlist('section')[index], classes=request.POST.getlist('classes')[index], date=request.POST.get('date') )

            name = 'subjects'+str(index+1)
            af = Attendance(
                student_id = Admission.objects.get(pk=request.POST.getlist('student_id')[index]),
                registration = request.POST.getlist('registration')[index],
                section = Section.objects.get(pk=request.POST.getlist('section')[index]),
                classes = Classes.objects.get(pk=request.POST.getlist('classes')[index]),
                date = request.POST.get('date'),
                subjects = request.POST.getlist(name),
                attendance_selection = request.POST.getlist('attendance_selection')[index],
                remarks = request.POST.getlist('remarks')[index],
                module_holder = module_holder
            )
            if selected.exists():
                # print('Already Exxit')
                selected.update(
                    student_id = Admission.objects.get(pk=request.POST.getlist('student_id')[index]),
                    registration = request.POST.getlist('registration')[index],
                    section = Section.objects.get(pk=request.POST.getlist('section')[index]),
                    classes = Classes.objects.get(pk=request.POST.getlist('classes')[index]),
                    date = request.POST.get('date'),
                    subjects = request.POST.getlist(name),
                    attendance_selection = request.POST.getlist('attendance_selection')[index],
                    remarks = request.POST.getlist('remarks')[index],
                   
                )
                messages.add_message(
                    request, messages.SUCCESS, 'Attendance details has been updated.',
                    fail_silently=True,
                )
                # messages.success(request, "Data Has been updated")
                # return redirect('student:attendance_search')
            else:
                af.save()
                print('Data Saved')
                # messages.success(request, "Attendance Has been Marked")
                messages.add_message(
                    request, messages.SUCCESS, 'Attendance details has been Marked.',
                    fail_silently=True,
                )
                # return redirect('student:attendance_search')
                

            index = index+1


        searched_stdents = Admission.objects.filter(module_holder=module_holder, admission_section=section, admission_class=classes)
        set_student_with_attendance = []
        for student in searched_stdents:
            d = Attendance.objects.values('attendance_selection','remarks','subjects').filter(module_holder=module_holder, student_id=student.pk, section=student.admission_section, classes=student.admission_class, date=date )
            # print(c[0][2],'=====================')
           
            handling_subjects = []
            subjects_object = Subject.objects.filter(module_holder=module_holder, class_name__contains=student.admission_class.pk)
            if d.exists():
                for sub in subjects_object:
                    if str(sub.pk) in str(d[0]['subjects']):
                        checked='checked="checked"'
                    else:
                        checked=''
                    handling_subjects.append({
                        'subject_name':sub.subject_name,
                        'pk': sub.pk,
                        'check': checked
                    })

                set_student_with_attendance.append(
                    {
                         'registration': student.admission_registration,
                         'date': date,
                         'student_id': Admission.objects.get(pk=student.pk),
                        'forms_details': AttendanceForm(
                            module_holder,
                                initial={
                                'registration': student.admission_registration,
                                'date': date,
                                'section': section,
                                'classes': classes,
                                'subjects': [sub.subject_name for sub in Subject.objects.filter(module_holder=module_holder, class_name=student.admission_class)],
                                'student_id': Admission.objects.get(pk=student.pk),
                                'attendance_selection':d[0]['attendance_selection'],
                                 'remarks': d[0]['remarks']
                                }
                            ),
                        'status': 'Marked',
                        'subjects': handling_subjects
                    }
                )
            else:
                for sub in subjects_object:
                    checked='checked="checked"'
                    handling_subjects.append({
                        'subject_name':sub.subject_name,
                        'pk': sub.pk,
                        'check': checked
                    })

                set_student_with_attendance.append(
                    {
                        'registration': student.admission_registration,
                        'date': date,
                        'student_id': Admission.objects.get(pk=student.pk),
                        'forms_details': AttendanceForm(
                            module_holder,
                                initial={
                                'registration': student.admission_registration,
                                'date': date,
                                'subjects': [sub.subject_name for sub in Subject.objects.filter(module_holder=module_holder, class_name=student.admission_class)],
                                'section': section,
                                'classes': classes,
                                'student_id': Admission.objects.get(pk=student.pk),
                               
                                
                                }
                            ),
                        'status': 'Not Marked',
                        'subjects': Subject.objects.filter(module_holder=module_holder, class_name__contains=student.admission_class.pk)
                    }
                )

        context = {
            'set_student_with_attendance': set_student_with_attendance,
            'attendance_date':date,
            'form': self.get_form()
        }
        return render(request, 'attendance/attendance_search_mark.html', context)

    # def form_valid(self, form):
    #     form.instane.module_holder='masood'
    #     form = super().form_invalid(form)
    #     return form

    # def get_form(self, **kwargs):
    #     form = super(AttendanceMark, self).get_form(**kwargs)
    #     form.fields['date'].widget = forms.TextInput(attrs={'type': 'date'})
    #     return form

    # def get_context_data(self, **kwargs):
    #     context = super(AttendanceMark, self).get_context_data(**kwargs)
    #     context['attendance_list'] = self.request
    #     context['form']=self.get_form()
    #     return context
