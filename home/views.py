from django.views.generic import CreateView, TemplateView, RedirectView, UpdateView, ListView
from academic.models import Subject, Classes, Routine, Section
from fee.models import Voucher
from payroll.models import Salary, Teacher
from django.utils import timezone
from django.db.models import Sum, Count, Q
from student.models import Attendance, Admission, StudentMark, MarkDistribution
from student.views import all_months, current_year
from student.forms import StudentMarkSearchForm, StudentMarkForm
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.dispatch import receiver
from django.contrib.auth import logout 
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.models import update_last_login
from .models import SchoolProfile, Setting, CsvFile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .decorators import unuthenticated_user, allowed_users
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, Permission, Group

from django.http import HttpResponse
from django.template import loader
import csv, io

from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from student.views import generate_reg
from django.utils import timezone

# from django.db.models.signals import post_save
# from .models import RegisterProfile
# home dashboard

def convert_month(month_val):
    if len(str(month_val))<2:
        return '0'+str(month_val)
    else:
        return month_val

def csvfile(request):
    # declaring template
    if request.user.is_staff:
        module_holder = request.user.username
    else:
        this_holder = Teacher.objects.get(user_ptr_id=request.user.id)
        module_holder = this_holder.module_holder

    template = "csv.html"
    data = CsvFile.objects.all()
   
    if request.method == "GET":
        return render(request, template)
    csv_file = request.FILES['csv']
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
  
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        classes = Classes.objects.filter(pk=column[1], module_holder=module_holder).first()
        # section = Section.objects.filter(pk=classes.section.pk, module_holder=module_holder)
        if classes:
            last_id = Admission.objects.filter(module_holder=module_holder).first()
            # print('last ID==================',last_id.admission_registration)
            if last_id is None:
                last_id = '0'
            else:
                last_id = last_id.admission_registration

            tution_fee = classes.fee
            discount = classes.discount
            after_detect_discount_fee_is = tution_fee-discount

            csv_data = Admission.objects.filter(
                    admission_date=column[0],
                    admission_class=classes,
                    admission_section=classes.section,
                    admission_registration=generate_reg(last_id),
                    name_of_student=column[8],
                    father_name=column[2],
                    father_cnic=column[3],
                    cast=column[6],
                    father_profession=column[7],
                    date_of_birth=column[9],
                    contact=column[5],
                    address=column[10],
                    gender=column[4],
                    recieve_admissin_fee_with_admission='0',
                    monthly_tution_fee=after_detect_discount_fee_is,
                    concession_fee=discount,
                    annual_fund=0,
                    free_student='0',
                    module_holder=module_holder,
                )
            
            # checking if any data exists
            get_already_saved_data = Admission.objects.filter(
                module_holder=module_holder,
                admission_date=column[0],
                admission_class=classes,
                name_of_student=column[8],
                father_name=column[2],
                father_cnic=column[3],
                date_of_birth=column[9]
            )
            if get_already_saved_data:
                csv_data.update()
               
            else:
                check = Admission(
                admission_date=column[0],
                admission_class=classes,
                admission_section=classes.section,
                admission_registration=generate_reg(last_id),
                name_of_student=column[8],
                father_name=column[2],
                father_cnic=column[3],
                cast=column[6],
                father_profession=column[7],
                date_of_birth=column[9],
                contact=column[5],
                address=column[10],
                gender=column[4],
                recieve_admissin_fee_with_admission='0',
                monthly_tution_fee=after_detect_discount_fee_is,
                concession_fee=discount,
                annual_fund=0,
                free_student='0',
                module_holder=module_holder
                ).save()
               


            # print('===============sadasd====', generate_reg(last_id))
            
            
        else:
            messages.warning(request, "ther are some invalid data. check class id or remove side spaces. in (date)")
            return redirect('student:admission_create')

    messages.success(request, "Students has been Added successfully!")
    return redirect('/student/admission/view/')
        # _, created = CsvFile.objects.update_or_create(
        #     name=column[0],
        #     email=column[1],
        #     address=column[2],
        #     phone=column[3],
        #     profile=column[4]
        # )
    context = {}
    
    
    return render(request, template, context)

def html_to_pdf_view(request):
    pass
    # paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']
    # html_string = render_to_string('core/pdf_template.html', {'paragraphs': paragraphs})

    # html = HTML(string=html_string)
    # html.write_pdf(target='/tmp/mypdf.pdf')

    # fs = FileSystemStorage('/tmp')
    # with fs.open('mypdf.pdf') as pdf:
    #     response = HttpResponse(pdf, content_type='application/pdf')
    #     response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
    #     return response
    # return response

class UserForm(UserCreationForm):
    email = forms.EmailField(label='Email (use active email for activation)', required=True)
    date_joined = forms.DateField(widget=forms.HiddenInput(attrs={'value': timezone.now().strftime('%Y-%m-%d')}))
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1', 
            'password2',
            'first_name',
            'last_name',
            'date_joined',
            
            ]

class SettingForm(forms.ModelForm):
    school_timing_from = forms.CharField(widget=forms.TextInput(attrs={'type': 'time'}))
    school_timing_to = forms.CharField(widget=forms.TextInput(attrs={'type': 'time'}))
    class Meta:
        model = Setting
        fields = '__all__'



# def ChangeSetting(request):
#     model = Setting
#     fields = [
#         'school_timing_from',
#         'school_timing_to'
#     ]
#     def form_valid(self, form):
#         form.instance.module_holder = self.request.user.username
#         return super().form_valid(form)



@login_required
def MainPage(request):
     # WORKING ON LOGIN GETTING SESSION 
    if request.user.is_staff:
        sp = SchoolProfile.objects.get(username=User.objects.get(pk=request.user.pk))
        request.session['school_user_id'] = sp.pk

    if request.user.is_staff:
        module_holder = request.user.username
    else:
        this_holder = Teacher.objects.get(user_ptr_id=request.user.id)
        module_holder = this_holder.module_holder

    # ECADEMIC START HETE
    total_teachers = Teacher.objects.filter(module_holder=module_holder).count()
    total_subject = Subject.objects.filter(module_holder=module_holder).count()
    total_class = Classes.objects.filter(module_holder=module_holder).count()
    total_coutine = Routine.objects.filter(module_holder=module_holder).count()

    all_data = {
        'total_teachers': total_teachers,
        'total_subject': total_subject,
        'total_class': total_class,
        'total_coutine': total_coutine
    }

    # START FEE & ACCOUNT START HERE
    month = timezone.now().strftime("%m")
    current_month = timezone.now().strftime("%Y-%m-%d")
    year = timezone.now().strftime("%Y")

    # GETTING MONTHLY FEE
    current_month_total_fee = Voucher.objects.filter(
        month=month,
        fee_month=current_month,
        year=year,
        module_holder=module_holder 
        ).aggregate(current_month_total_fee=Sum('monthly_tution_fee_paid'))

    # GETTING YEALY FEE
    current_year_total_fee = Voucher.objects.filter(
        year=year,
        module_holder=module_holder
        ).aggregate(current_year_total_fee=Sum('monthly_tution_fee_paid'))
    
    # GETTING MONTHLY SALARY TOTAL
    current_month_total_salary = Salary.objects.filter(
        Q(Salary_date__startswith=timezone.now().strftime('%Y-%m'),
        module_holder=module_holder)
        ).aggregate(monthly_salary=Sum('salary'))

    # GETTING yearly SALARY TOTAL
    current_year_total_salary = Salary.objects.filter(
        Q(Salary_date__startswith=timezone.now().strftime('%Y'),
        module_holder=module_holder)
        ).aggregate(yearly_salary=Sum('salary'))

    data_chart= []
    for month in range(1, 13):
        paid =  Voucher.objects.filter(module_holder=module_holder, year=year, month=convert_month(month), monthly_tution_fee_paid__gt=1).aggregate(paid = Sum('monthly_tution_fee_paid'))
        unpaid = Voucher.objects.filter(module_holder=module_holder, year=year, month=convert_month(month), monthly_tution_fee_paid__lt=1).aggregate(unpaid = Sum('monthly_tution_fee') )
        
        data_chart.append({
            'paid': paid,
            'unpaid': unpaid,
            'date': year+'-'+str(convert_month(month))+'-'+'01'
        })
    final_chart=[]
    for data in data_chart:
        if data['paid']['paid'] is None:
            paid = 0
        else:
            paid = data['paid']['paid']

        if data['unpaid']['unpaid'] is None:
            unpaid = 0
        else:
            unpaid = data['unpaid']['unpaid']
        final_chart.append({
            'paid_amount': paid,
            'un_paid_amount': unpaid,
            'date': data['date'],
            
        })
        
    ddddd = json.dumps(final_chart)
    fee_context = {
        'data_chart': final_chart,
        'ddddd': ddddd,
        'current_year_total_salary':current_year_total_salary,
        'current_month_total_salary': current_month_total_salary,
        'current_month_total_fee': current_month_total_fee,
        'current_year_total_fee': current_year_total_fee,
        'current_month': timezone.now().strftime('%B, %Y'),
        'current_month_redirect': timezone.now().strftime('%Y-%m-%d'),
        'current_year': timezone.now().strftime('%Y'),
        'current_month_total_fee': current_month_total_fee
    }

    # START STUDENT DATA OR 
    monthly_chart_data =[] 
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
    dropout_yearly = Admission.objects.filter(module_holder=module_holder, status_date__startswith=current_year).count() 

    chart_data_yearly = {
        'students_yearly': students_yearly,
        'present_yearly': present_yearly,
        'absent_yearly': absent_yearly,
        'leave_yearly': leave_yearly,
        'latin_yearly': latin_yearly,
        'dropout_yearly': dropout_yearly

    }
    profile = SchoolProfile.objects.get(username=request.user, module_holder=module_holder)
    request.session['school_logo'] = str(profile.school_logo.url)
    # print( profile.school_logo.url)

    context = {
        'all_data': all_data,
        'fee_data': fee_context,
        'chart_data_monthly': json.dumps(monthly_chart_data),
        'chart_data_yearly': chart_data_yearly,
        'current_year': current_year,
       
    }
    return render(request, 'index.html', context)

   
# def Register(request):
#     if request.method=='POST':
#         form = UserForm(request.POST,  initial={'is_staff':True, 'groups':1})
#         if form.is_valid():
#             form.save()
#             Group.objects.get(name='school_user')
#             messages.success(request, 'Your Registration has been Success. Please login to proceed')
#             return redirect('home:login')
#     else:
#         form = UserForm( initial={'is_staff':True, 'groups':1})
    
#     context = {
#         'form': form
#     }
#     return render(request, 'registration/register.html', context)


class Register(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'registration/register.html'
    form_class = UserForm

    def form_valid(self, form):
        form.instance.is_staff = True
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

    success_url = reverse_lazy('home:login')
    success_message = 'Your Registration has been Success. Please login to proceed'


class SchoolProfiles(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'user_profile.html'
    permission_required = 'home.change_schoolprofile'
    
    model = SchoolProfile
    fields = [
        'contact_no',
        'cnic',
        'school_name',
        'school_logo',
        'school_registration_no',
        'address',
        'school_timing_from',
        'school_timing_to',
        'email_address'
    ]    

    login_url = 'home:login'

    def get_form(self, **kwargs):
        form = super(SchoolProfiles, self).get_form(**kwargs)
        form.fields['school_timing_from'].widget = forms.TextInput(attrs={'type': 'time'})
        form.fields['school_timing_to'].widget = forms.TextInput(attrs={'type': 'time'})
        return form

    def get_context_data(self, *args, **kwargs):
        context = super(SchoolProfiles, self).get_context_data(**kwargs)
        module_holder = self.request.user.username
        all_user_perms = User.get_group_permissions(self.request.user)
        # print(all_user_perms,'==========================================================================loginded======')
        # self.request.success['school_profile_id'] = SchoolProfile.objects.get(pk=kwargs['pk'])
        context['school_profile_data'] = SchoolProfile.objects.filter(pk=self.kwargs['pk']).first()
        context['user_profile_data'] = User.objects.get(pk=self.request.user.pk)
        context['userprofileform'] = '/profile/profile/'+str(self.kwargs['pk'])+'/complete'
        return context  


class LogoutView(RedirectView):
    url = '/'
    def get(self, request, **kwargs):
        if request.session.get('school_user_id',''):
                del request.session['school_user_id']
        logout(request)
        return super(LogoutView, self).get(request, **kwargs)
