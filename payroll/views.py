from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import  CreateView, UpdateView, DeleteView, ListView, TemplateView
# Create your views here.
from .forms import TeacherForm, SalaryForm, FeeDefSerchForm, SchedualForm
from .models import Teacher, Salary, Schedual, Position, Leave, EmployeeAttendance, AdvanceSalary
from django.db.models import Q, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from home.decorators import unuthenticated_user, allowed_users
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, Permission, Group
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone
from django import forms
from datetime import datetime, time, date, timedelta
from calendar import monthrange
from fee.views import convert_month
from django.db.models.functions import Coalesce
from num2words import num2words
from django.contrib import messages
# Payroll section


class SearchDateForm(forms.Form):

    seacher_date = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'type': 'month',
                'value': timezone.now().strftime('%Y-%m-%d')
            }
        )
    )


def time_diff(time_str1, time_str2):
    t1 = datetime.strptime(time_str1, '%H:%M')
    t2 = datetime.strptime(time_str2, '%H:%M')
    dt = abs(t2 - t1)
    return time(dt.seconds // 3600, (dt.seconds // 60) % 60).strftime('%H:%M')


def get_all_says(year, month):
   m = date(year, month, 1)                    # January 1st
   m += timedelta(days = 6 - m.weekday())  # First Sunday
   while m.month == month:
      yield m
      m += timedelta(days = 7)


def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

def convert_month_into_string(number):
    if number is 1:
        return 'Jan'
    elif number is 2:
        return 'Feb'
    elif number is 3:
        return 'Mar'
    elif number is 4:
        return 'Apr'
    elif number is 5:
        return 'May'
    elif number is 6:
        return 'Jun'
    elif number is 7:
        return 'Jul'
    elif number is 8:
        return 'Aug'
    elif number is 9:
        return 'Sep'
    elif number is 10:
        return 'Oct'
    elif number is 11:
        return 'Nov'
    elif number is 12:
        return 'Dec'
    else:
        return 'invalid'


class EmployeeAttednaceCreate(SuccessMessageMixin ,CreateView):
    model = EmployeeAttendance
    fields = ['employee_name', 'date', 'time_in', 'time_out',]
    template_name = 'payroll/attendance_add.html'
    success_message = 'Attendance has been marked'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.instance.module_holder = module_holder
        return super().form_valid(form)

    def get_form(self, **kwargs):
        form = super(EmployeeAttednaceCreate, self).get_form(**kwargs)
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.fields['employee_name'].queryset = Teacher.objects.filter(module_holder=module_holder)
        form.fields['date'].widget.attrs={'class': 'date', 'autocomplete': 'off'} 
        form.fields['time_in'].widget = forms.TextInput(attrs={'type':'time'}) 
        form.fields['time_out'].widget = forms.TextInput(attrs={'type':'time'}) 
        return form


class EmployeeAttednaceUpdate(SuccessMessageMixin ,UpdateView):
    model = EmployeeAttendance
    fields = ['employee_name', 'date', 'time_in', 'time_out',]
    template_name = 'payroll/attendance_add.html'
    success_message = 'Attendance has been Updated'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.instance.module_holder = module_holder
        return super().form_valid(form)

    def get_form(self, **kwargs):
        form = super(EmployeeAttednaceUpdate, self).get_form(**kwargs)
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.fields['employee_name'].queryset = Teacher.objects.filter(module_holder=module_holder)
        form.fields['date'].widget.attrs={'class': 'date', 'autocomplete': 'off'} 
        form.fields['time_in'].widget = forms.TextInput(attrs={'type':'time'}) 
        form.fields['time_out'].widget = forms.TextInput(attrs={'type':'time'}) 
        return form

   

def employee_induigual(request, pk):
    module_holder = request.user.username
    employee = Teacher.objects.get(module_holder=module_holder, pk=pk)
    current_year = timezone.now().strftime('%Y')
    current_month = timezone.now().strftime('%m')
    current_day = timezone.now().strftime('%d')

    if request.method=='POST':
        print(request.POST,'==========sds=dasdasdasdasdsdd==')
        current_year = request.POST.get('seacher_date')[:4]
        searchdateform = SearchDateForm(request.POST)
    else:
        searchdateform = SearchDateForm()
    
    heading = []
    holidays = [] 
    leaves = []

       
    whole_year = []
    for month in range(1, 13):
        sundays = []
        for sunday in get_all_says(int(current_year), int(month)):
            sundays.append(sunday.day)

        count_of_date_searched = int(current_year)+int(month)
        atte_status = []
        num_of_days = monthrange(int(current_year),int(month))[1]
        for day in range(1, num_of_days+1):
            try:
                hds = Leave.objects.values('from_date','to_date').filter(employee=Teacher.objects.get(pk=pk), type='h')
                for hd in hds:
                    startdate = hd['from_date']
                    enddate = hd['to_date']
                    for days in daterange(startdate, enddate):
                        holidays.append(str(days.year)+'-'+str(convert_month(days.month))+'-'+str(convert_month(days.day)))
            except Exception as ex:
                holidays = []

            try:
                lvs = Leave.objects.values('from_date','to_date').filter(employee=Teacher.objects.get(pk=pk), type='l')
                for lv in lvs:
                    startdate = lv['from_date']
                    enddate = lv['to_date']
                    for days in daterange(startdate, enddate):
                        leaves.append(str(days.year)+'-'+str(convert_month(days.month))+'-'+str(convert_month(days.day)))
            except Exception as ex:
                leaves = []

            
            heading = []
            count_of_date_searched =count_of_date_searched+1
            holiday_murging = str(current_year)+'-'+str(convert_month(month))+'-'+str(convert_month(day))
            print(holiday_murging,'===============================holuddd')
            sun_or_other_day = ''
            if day in sundays:
                sun_or_other_day = 's'
            elif holiday_murging in holidays:
                sun_or_other_day = 'h'
            elif holiday_murging in leaves:
                sun_or_other_day = 'l'
            else:
                if date(int(current_year), int(convert_month(month)), day) <= date(int(timezone.now().strftime('%Y')), int(convert_month(current_month)), int(current_day)):
                    att_got = EmployeeAttendance.objects.filter(
                            module_holder=module_holder,
                            employee_name=employee,
                            date=date(int(current_year), int(convert_month(month)), day)
                    )
                    if att_got:
                        sun_or_other_day = 'p'
                    else:
                        sun_or_other_day = 'a'
                else:
                    sun_or_other_day='n'

                heading.append({'day': day})
            atte_status.append({'sun_or_other_day': sun_or_other_day, 'date': day})
            # print(sun_or_other_day,'================',date(int(current_year), int(current_month), day)) 
        whole_year.append({
         
                'month': convert_month_into_string(month),
                'employee': employee,
                'atte_status':atte_status,
                
                
            })
        
    # print(whole_year,'======')
    context = {
        'heading': range(1,32),
        'SearchDateForm': searchdateform,
        'whole_years': whole_year
    }
    return render(request, 'payroll/attendance_ind.html', context)


#  ATEENDANCE STARTS HERE
def employee_attendance(request):
    module_holder = request.user.username
    current_year = timezone.now().strftime('%Y')
    current_month = timezone.now().strftime('%m')
    current_day = timezone.now().strftime('%d')
    sundays = []
    
    for sunday in get_all_says(int(current_year), int(current_month)):
        sundays.append(sunday.day)

    emploies = Teacher.objects.filter(module_holder=module_holder)
    all_emp_att = []
    heading = []
    for employee in emploies:
        holidays = []
        leaves = []
        
        try:
            # hd1 = hd['from_date']
            hds = Leave.objects.values('from_date','to_date').filter(employee=employee, type='h')
            for hd in hds:
                print(hd,'====', employee)
                startdate = hd['from_date']
                enddate = hd['to_date']
                for days in daterange(startdate, enddate):
                    holidays.append(str(days.year)+'-'+str(convert_month(days.month))+'-'+str(convert_month(days.day)))
        except Exception as ex:
            holidays = []

        try:
            # hd1 = hd['from_date']
            lvs = Leave.objects.values('from_date','to_date').filter(employee=employee, type='l')
            for lv in lvs:
                startdate = lv['from_date']
                enddate = lv['to_date']
                for days in daterange(startdate, enddate):
                    leaves.append(str(days.year)+'-'+str(convert_month(days.month))+'-'+str(convert_month(days.day)))
        except Exception as ex:
            leaves = []
        
            
        atte_status = []
        heading = []
        pk = 0
        for day in range(1, monthrange(int(current_year),int(current_month))[1]+1):
            holiday_murging = str(current_year)+'-'+str(current_month)+'-'+str(convert_month(day))
           
            sun_or_other_day = ''
            if day in sundays:
                sun_or_other_day = 's'
            elif holiday_murging in holidays:
                sun_or_other_day = 'h'
            elif holiday_murging in leaves:
                sun_or_other_day = 'l'
            else:
                if date(int(current_year), int(current_month), day) <= date(int(timezone.now().strftime('%Y')), int(current_month), int(current_day)):
                    att_got = EmployeeAttendance.objects.filter(
                            module_holder=module_holder,
                            employee_name=employee,
                            date=date(int(current_year), int(current_month), day)
                    ).first()
                    # print('commoing in else', date(int(current_year), int(current_month), day))
                    if att_got:
                        sun_or_other_day = 'p'
                        pk = att_got.pk
                    else:
                        sun_or_other_day = 'a'
                else:
                    sun_or_other_day='n'
            heading.append({'day': day, 'status': sun_or_other_day })
            atte_status.append({'sun_or_other_day': sun_or_other_day,'pk':pk})
            # print(sun_or_other_day,'================',date(int(current_year), int(current_month), day)) 
        all_emp_att.append({
                'employee': employee,
                'atte_status':atte_status,
            })
    
    context = {
        'all_emp_att':all_emp_att,
        'heading': heading
    }
    return render(request, 'payroll/attendance.html', context)

# ATTENDANCE ENDS HERE


# POSTIONS STARTS HERE
class LeaveView(LoginRequiredMixin, ListView):
    # permission_required = 'payroll.view_leave'
    model = Leave
    login_url = 'home:login'
    template_name = 'payroll/leave.html'
    success_message = 'leave has been created!'

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        context = super(LeaveView, self).get_context_data(**kwargs)
        context['leaves'] = Leave.objects.filter(module_holder=module_holder)
        return context


class LeaveCreate(LoginRequiredMixin , SuccessMessageMixin ,CreateView):
    # permission_required = 'academic.add_leave'
    success_message = 'leave has been created!'

    model = Leave
    fields = [
        'employee',
        'date',
        'type',
        'is_paid',
        'from_date',
        'to_date',
        'reasion',
        'leave_message'
    ]
    login_url = 'home:lgoin'
    template_name = 'payroll/leave_add.html'

   
    def post(self, request):
        module_holder = request.user.username
        for emp in request.POST.getlist('employee'):
            save_leave = Leave(
                employee = Teacher.objects.get(pk=emp),
                date = request.POST.get('date'),
                type = request.POST.get('type'),
                from_date = request.POST.get('from_date'),
                to_date = request.POST.get('to_date'),
                reasion = request.POST.get('reasion'),
                leave_message = request.POST.get('leave_message'),
                module_holder = module_holder
            )
            leave = Leave.objects.filter(
                employee = Teacher.objects.get(pk=emp),
                date = request.POST.get('date'),
                from_date = request.POST.get('from_date'),
                to_date = request.POST.get('to_date'),
            )
            print(leave)
            if leave:               
                print('data has been saved ==========================yes saved data')
            else:
                save_leave.save()
                # print('data has been not saved ==========================no saved data')

        return redirect('payroll:leave_view')

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
        form = super(LeaveCreate, self).get_form(**kwargs)
        form.fields['date'].widget = forms.TextInput(attrs={'class':'date'})    
        form.fields['from_date'].widget = forms.TextInput(attrs={'class':'date'})    
        form.fields['to_date'].widget = forms.TextInput(attrs={'class':'date'})  
        form.fields['employee'].widget.attrs = {'class': 'basic-multiple', 'multiple': 'multiple'}
        form.fields['is_paid'].widget.attrs = {'class': 'customSwitch1'}
        form.fields['employee'].queryset = Teacher.objects.filter(module_holder=module_holder)

        return form  


class LeaveUpdate(LoginRequiredMixin, SuccessMessageMixin  ,UpdateView):
    # permission_required = 'academic.change_classes'
    model = Leave
    fields = [
        'employee',
        'date',
        'type',
        'is_paid',
        'from_date',
        'to_date',
        'reasion',
        'leave_message'
    ]
    login_url = 'home:lgoin'
    template_name = 'payroll/leave_add.html'
    success_message = 'leave has been updated!'

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
        form = super(LeaveUpdate, self).get_form(**kwargs)
        form.fields['date'].widget = forms.TextInput(attrs={'class':'date'})    
        form.fields['from_date'].widget = forms.TextInput(attrs={'class':'date'})    
        form.fields['to_date'].widget = forms.TextInput(attrs={'class':'date'})    
        form.fields['employee'].queryset = Teacher.objects.filter(module_holder=module_holder)
        return form  

class LeaveDelete(LoginRequiredMixin, DeleteView):
    login_url = 'home:lgoin'
    # permission_required = 'academic.delete_classes'
    model = Leave
    success_url = reverse_lazy('payroll:leave_view')
# leave ENDS HERE


# SCHADUAL STARTS HRERE
# STRAT CLASSES HERE
class SchedualView(LoginRequiredMixin, ListView):
    # permission_required = 'payroll.view_Schedual'
    model = Schedual
    login_url = 'home:login'
    # context_object_name = 'classes'
    template_name = 'payroll/schedual.html'
    success_message = 'Time Schedual has been created!'

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        context = super(SchedualView, self).get_context_data(**kwargs)
        context['scheduals'] = Schedual.objects.filter(module_holder=module_holder)
        return context

class SchedualCreate(LoginRequiredMixin , SuccessMessageMixin ,CreateView):
    # permission_required = 'academic.add_Schedual'
    success_message = 'Time Schedual has been created!'
    model = Schedual
    fields = [
        'time_in',
        'time_out'
    ]
    login_url = 'home:lgoin'
    template_name = 'payroll/schedual_add.html'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.instance.module_holder = module_holder
        return super().form_valid(form)  

    def get_form(self, **kwargs):
        form = super(SchedualCreate, self).get_form(**kwargs)
        form.fields['time_in'].widget = forms.TextInput(attrs={'type':'time'})    
        form.fields['time_out'].widget = forms.TextInput(attrs={'type':'time'})    
        return form  


class SchedualUpdate(LoginRequiredMixin, SuccessMessageMixin  ,UpdateView):
    # permission_required = 'academic.change_classes'
    model = Schedual
    fields = [
        'time_in',
        'time_out'
    ]
    login_url = 'home:lgoin'
    template_name = 'payroll/schedual_add.html'
    success_message = 'Time schedual has been updated!'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.instance.module_holder = module_holder
        resolver = super().form_valid(form)
        if self.request.is_ajax():
            schedual = Schedual.objects.filter(module_holder=module_holder).order_by('-id').first()
            data = {
                'pk': schedual.pk,
                'name': schedual.time_in+''+schedual.time_out,
                
            }
            return JsonResponse(data)
        else:
            return resolver

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({'status': 'already'})
        return response

    def get_form(self, **kwargs):
        form = super(SchedualUpdate, self).get_form(**kwargs)
        form.fields['time_in'].widget = forms.TextInput(attrs={'type':'time'})    
        form.fields['time_out'].widget = forms.TextInput(attrs={'type':'time'})    
        return form  

class SchedualDelete(LoginRequiredMixin, DeleteView):
    login_url = 'home:lgoin'
    # permission_required = 'academic.delete_classes'
    model = Schedual
    success_url = reverse_lazy('payroll:schedual_view')

# SCHADUAL ENDS HERE

# POSTIONS STARTS HERE
class PositionView(LoginRequiredMixin, ListView):
    # permission_required = 'payroll.view_position'
    model = Position
    login_url = 'home:login'
    template_name = 'payroll/position.html'
    success_message = 'position has been created!'

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        context = super(PositionView, self).get_context_data(**kwargs)
        context['positions'] = Position.objects.filter(module_holder=module_holder)
        return context


class PositionCreate(LoginRequiredMixin , SuccessMessageMixin ,CreateView):
    # permission_required = 'academic.add_position'
    success_message = 'Position has been created!'

    model = Position
    fields = [
        'position_title',
        'rate_per_hour'
    ]
    login_url = 'home:lgoin'
    template_name = 'payroll/position_add.html'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.instance.module_holder = module_holder
        return super().form_valid(form)  

    # def get_form(self, **kwargs):
    #     form = super(PositionCreate, self).get_form(**kwargs)
    #     form.fields['time_in'].widget = forms.TextInput(attrs={'type':'time'})    
    #     form.fields['time_out'].widget = forms.TextInput(attrs={'type':'time'})    
    #     return form  


class PositionUpdate(LoginRequiredMixin, SuccessMessageMixin  ,UpdateView):
    # permission_required = 'academic.change_classes'
    model = Position
    fields = [
        'position_title',
        'rate_per_hour'
    ]
    login_url = 'home:lgoin'
    template_name = 'payroll/position_add.html'
    success_message = 'position has been updated!'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.instance.module_holder = module_holder
        return super().form_valid(form)

    # def get_form(self, **kwargs):
    #     form = super(positionUpdate, self).get_form(**kwargs)
    #     form.fields['time_in'].widget = forms.TextInput(attrs={'type':'time'})    
    #     form.fields['time_out'].widget = forms.TextInput(attrs={'type':'time'})    
    #     return form  

class PositionDelete(LoginRequiredMixin, DeleteView):
    login_url = 'home:lgoin'
    # permission_required = 'academic.delete_classes'
    model = Position
    success_url = reverse_lazy('payroll:position_view')
# POSITION ENDS HERE

class TeacherView(PermissionRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = Teacher
    login_url = 'home:lgoin'
    template_name = 'payroll/teacher.html'
    permission_required = 'payroll.view_teacher'
    success_message = 'Teacher has been added!'

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        context = super(TeacherView, self).get_context_data(**kwargs)
        context['teachers'] = Teacher.objects.filter(module_holder=module_holder)
        return context


class TeacherCreate(LoginRequiredMixin ,PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Teacher
    form_class = TeacherForm
    login_url = 'home:lgoin'
    template_name = 'payroll/teacher_add.html'
    success_message = 'Teacher has been created successfully!'
    permission_required = 'payroll.add_teacher'
    # success_url = '/payroll/teacher/create/'

    def form_valid(self, form): 
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.instance.module_holder = module_holder
        # last_user = Teacher.objects.all('username').last()
        self.group_got, self.created_got = Group.objects.get_or_create(name=self.request.POST.get('username'))
        if self.created_got or self.group_got:
            for perms in self.request.POST.getlist('perms'):
                self.group_got.permissions.add(int(perms))
                
        return super().form_valid(form)

    def get_success_url(self):
        lastUser = User.objects.latest('id')   
        url = self.object.get_absolute_url()     
        # print(lastUser,'===============last user ===== in get success============')
        # print(self.objects,'=============================')
        lastUser.groups.add(self.group_got)
        return url

    def get_form(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form = super(TeacherCreate, self).get_form(**kwargs)
        form.fields['date_of_birth'].widget = forms.TextInput( attrs = {'type': 'date'})
        form.fields['date_of_join'].widget = forms.TextInput( attrs = {'type': 'date'})
        form.fields['time_schedual'].queryset = Schedual.objects.filter(module_holder=module_holder)
        form.fields['position'].queryset = Position.objects.filter(module_holder=module_holder)
        form.fields['time_schedual'].widget.attrs={'class': 'basic-multiple'}
        form.fields['position'].widget.attrs={'class': 'basic-multiple'}
        form.fields['gender'].widget = forms.RadioSelect()

        return form

    def get_context_data(self, **kwargs):
        collect_without_dot = []
        collect_murged_sorted = []
        context = super(TeacherCreate, self).get_context_data(**kwargs)
        all_user_perms = User.get_group_permissions(self.request.user)

        for groups in all_user_perms:
            collect_without_dot.append(groups.split('.')[1].split('_')[1])
        
        collect_without_dot = sorted(collect_without_dot)

        header_prevent_dup = set(collect_without_dot)
        header_sorted = sorted(header_prevent_dup)

        LIST_OF_CATEGORYS = ['add', 'change', 'view', 'delete']

        for LIST_OF_CATEGORY in LIST_OF_CATEGORYS:
            binded = []
            for header_sort in header_sorted:
                all_perms = Permission.objects.values('id', 'codename').filter(codename=LIST_OF_CATEGORY+'_'+header_sort)
                val = all_perms[0]['codename'].split('_')[1]
                binded.append({
                   'id': all_perms[0]['id'],
                   'codename': val
                })
            collect_murged_sorted.append({
                    'head': LIST_OF_CATEGORY,
                    'values': binded
                })

        # print(collect_murged_sorted,'================== after sorted')
        context['all_school_user_perm_list'] = collect_murged_sorted
        context['header_sorted']=header_sorted
        context['teachercreateurl'] = '/payroll/teacher/create'
        # context['category'] = LIST_OF_CATEGORY
        return context


class TeacherUpdate(LoginRequiredMixin ,PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'payroll/teacher_add.html'
    success_message = 'Teacher has been created successfully!'
    permission_required = 'payroll.change_teacher'
    login_url = 'home:lgoin'
    success_message = 'Teacher has been Updated!'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.instance.module_holder = module_holder
        # last_user = Teacher.objects.all('username').last()
        self.group_got, self.created_got = Group.objects.get_or_create(name=self.request.POST.get('username'))
        if self.created_got or self.group_got:
            for perms in self.request.POST.getlist('perms'):
                self.group_got.permissions.add(int(perms))
                
        return super().form_valid(form)

    def get_success_url(self):
        lastUser = User.objects.latest('id')   
        url = self.object.get_absolute_url()     
        # print(lastUser,'===============last user ===== in get success============')
        # print(self.objects,'=============================')
        lastUser.groups.add(self.group_got)
        return url

    def get_form(self, **kwargs):
        form = super(TeacherUpdate, self).get_form(**kwargs)
        form.fields['date_of_birth'].widget = forms.TextInput( attrs = {'type': 'date'})
        form.fields['date_of_join'].widget = forms.TextInput( attrs = {'type': 'date'})
        form.fields['gender'].widget = forms.RadioSelect()
        return form
    
    def get_context_data(self, **kwargs):
        collect_without_dot = []
        collect_murged_sorted = []
        context = super(TeacherUpdate, self).get_context_data(**kwargs)
        all_user_perms = User.get_group_permissions(self.request.user)

        for groups in all_user_perms:
            collect_without_dot.append(groups.split('.')[1].split('_')[1])
        
        collect_without_dot = sorted(collect_without_dot)

        header_prevent_dup = set(collect_without_dot)
        header_sorted = sorted(header_prevent_dup)

        LIST_OF_CATEGORYS = ['add', 'change', 'view', 'delete']

        for LIST_OF_CATEGORY in LIST_OF_CATEGORYS:
            binded = []
            for header_sort in header_sorted:
                all_perms = Permission.objects.values('id', 'codename').filter(codename=LIST_OF_CATEGORY+'_'+header_sort)
                val = all_perms[0]['codename'].split('_')[1]
                binded.append({
                   'id': all_perms[0]['id'],
                   'codename': val
                })
            collect_murged_sorted.append({
                    'head': LIST_OF_CATEGORY,
                    'values': binded
                })
            

        print(collect_murged_sorted,'================== after sorted')
        context['all_school_user_perm_list'] = collect_murged_sorted
        context['header_sorted']=header_sorted
        context['teachercreateurl'] = '/payroll/payroll/teacher/'+str(self.kwargs.get('pk'))+'/update/'
        # context['category'] = LIST_OF_CATEGORY
        return context


class TeacherDelete(LoginRequiredMixin ,PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'payroll.delete_teacher'
    success_message = 'Teacher has been deleted'
    model = Teacher
    success_url = reverse_lazy('payroll:teacher_view')
    login_url = 'home:lgoin'


@login_required
@allowed_users('view_salary')
def manage_salary(request):
    module_holder = request.user.username
    current_year = timezone.now().strftime('%Y')
    current_month = timezone.now().strftime('%m')
    current_day = timezone.now().strftime('%d')

    if request.method=='POST':
        index = 0
        for data in request.POST.getlist('yes_salary'):
            salary_object = Salary.objects.filter(
                 employee_name=Teacher.objects.get(pk=request.POST.getlist('employee_name')[int(request.POST.getlist('yes_salary')[index])-1]),
                 Salary_date=request.POST.getlist('Salary_date')[int(request.POST.getlist('yes_salary')[index])-1]
            )
            
            if len(salary_object)>0:
                Salary.objects.filter(
                 employee_name=Teacher.objects.get(pk=request.POST.getlist('employee_name')[int(request.POST.getlist('yes_salary')[index])-1]),
                 Salary_date=request.POST.getlist('Salary_date')[int(request.POST.getlist('yes_salary')[index])-1]
                ).update(
                    Salary_release_date=request.POST.getlist('Salary_release_date')[int(request.POST.getlist('yes_salary')[index])-1],
                    salary=request.POST.getlist('salary')[int(request.POST.getlist('yes_salary')[index])-1],
                    bonus=request.POST.getlist('bonus')[int(request.POST.getlist('yes_salary')[index])-1],
                    advance_detected=request.POST.getlist('advance_detected')[int(request.POST.getlist('yes_salary')[index])-1],
                    other=request.POST.getlist('other')[int(request.POST.getlist('yes_salary')[index])-1],
                    details=request.POST.getlist('details')[int(request.POST.getlist('yes_salary')[index])-1],
                    module_holder= module_holder
                )
            else:
                Salary(
                    employee_name=Teacher.objects.get(pk=request.POST.getlist('employee_name')[int(request.POST.getlist('yes_salary')[index])-1]),
                    Salary_date=request.POST.getlist('Salary_date')[int(request.POST.getlist('yes_salary')[index])-1],
                    Salary_release_date=request.POST.getlist('Salary_release_date')[int(request.POST.getlist('yes_salary')[index])-1],
                    salary=request.POST.getlist('salary')[int(request.POST.getlist('yes_salary')[index])-1],
                    bonus=request.POST.getlist('bonus')[int(request.POST.getlist('yes_salary')[index])-1],
                    advance_detected=request.POST.getlist('advance_detected')[int(request.POST.getlist('yes_salary')[index])-1],
                    other=request.POST.getlist('other')[int(request.POST.getlist('yes_salary')[index])-1],
                    details=request.POST.getlist('details')[int(request.POST.getlist('yes_salary')[index])-1],
                    module_holder= module_holder
                ).save()
            index = index+1


    employee_form_data = []
    module_holder = request.user.username
    teachers = Teacher.objects.filter(module_holder=module_holder)
    for teacher in teachers:
        salary_object = Salary.objects.filter(
                Q(employee_name=Teacher.objects.get(pk=teacher.pk),
                 Salary_date__startswith=timezone.now().strftime('%Y-%m'),
                 module_holder=module_holder
                 )
            ).first()
        
        status = 0
        if salary_object:
            salary_pk = salary_object.pk
            status = salary_object.salary
        else:
            salary_pk = 0
            status = 0

        advance_amount = AdvanceSalary.objects.values('advance_amount').filter(employee_name=teacher, module_holder=module_holder).aggregate(total_advance=Coalesce(Sum('advance_amount'), 0))
        detected_amount = Salary.objects.filter(employee_name=teacher, module_holder=module_holder).aggregate(detected_amount=Coalesce(Sum('advance_detected'),0))
        
        advance_taken = 0
        advance_retured = 0
        still_remaining = 0

        if int(advance_amount['total_advance']) > int(detected_amount['detected_amount']):
            advance_taken = advance_amount
            advance_retured = detected_amount
            still_remaining = int(advance_amount['total_advance'])-int(detected_amount['detected_amount'])

        monthly_detection = AdvanceSalary.objects.values('monthly_detection').filter(employee_name=teacher, module_holder=module_holder).aggregate(monthly_detection=Coalesce(Sum('monthly_detection'), 0))

        if still_remaining < int(monthly_detection['monthly_detection']):
            monthly_detect = still_remaining
        else:
            monthly_detect = int(monthly_detection['monthly_detection']) 

        # START WORKING WITH SALARY
        hourly_rate = Position.objects.get(pk=teacher.position_id, module_holder=module_holder)
        present_days = [] 
        sundays = []
        for sunday in get_all_says(int(current_year), int(current_month)):
            sundays.append(sunday.day)

        count_of_date_searched = int(current_year)+int(current_month)
        atte_status = []
        holidays = []
        leaves = []
        num_of_days = monthrange(int(current_year),int(current_month))[1]
        for day in range(1, num_of_days+1):
            try:
                hds = Leave.objects.values('from_date','to_date').filter(employee=teacher, type='h')
                for hd in hds:
                    startdate = hd['from_date']
                    enddate = hd['to_date']
                    for days in daterange(startdate, enddate):
                        holidays.append(str(days.year)+'-'+str(convert_month(days.month))+'-'+str(convert_month(days.day)))
            except Exception as ex:
                holidays = []
            
            try:
                lvs = Leave.objects.values('from_date','to_date').filter(employee=teacher, type='l')
                for lv in lvs:
                    startdate = lv['from_date']
                    enddate = lv['to_date']
                    for days in daterange(startdate, enddate):
                        leaves.append(str(days.year)+'-'+str(convert_month(days.month))+'-'+str(convert_month(days.day)))
            except Exception as ex:
                leaves = []

            
            heading = []
            count_of_date_searched =count_of_date_searched+1
            holiday_murging = str(current_year)+'-'+str(current_month)+'-'+str(convert_month(day))
            # print(holiday_murging,'===============================holuddd')
            
            sun_or_other_day = ''
            if day in sundays:
                # hours = Schedual.objects.get(module_holder=module_holder, pk=teacher.time_schedual.pk)
                # t1 = datetime.strptime(hours.time_in, '%H:%M')
                # t2 = datetime.strptime(hours.time_out, '%H:%M')
                # t1 = datetime.strftime(t1, '%H:%M')
                # t2 = datetime.strftime(t2, '%H:%M')
                # hours = time_diff(t1, t2)
                # present_days.append({'hours': hours, 'date': date(int(current_year), int(current_month), day), 'emp': teacher})
                sun_or_other_day = 's'
            elif holiday_murging in leaves:
                hours = Schedual.objects.get(module_holder=module_holder, pk=teacher.time_schedual.pk)
                t1 = datetime.strptime(hours.time_in, '%H:%M')
                t2 = datetime.strptime(hours.time_out, '%H:%M')
                t1 = datetime.strftime(t1, '%H:%M')
                t2 = datetime.strftime(t2, '%H:%M')
                hours = time_diff(t1, t2)
                present_days.append({'hours': hours, 'date': date(int(current_year), int(current_month), day), 'emp': teacher})

            elif holiday_murging in holidays:
                hours = Schedual.objects.get(module_holder=module_holder, pk=teacher.time_schedual.pk)
                t1 = datetime.strptime(hours.time_in, '%H:%M')
                t2 = datetime.strptime(hours.time_out, '%H:%M')
                t1 = datetime.strftime(t1, '%H:%M')
                t2 = datetime.strftime(t2, '%H:%M')
                hours = time_diff(t1, t2)
                present_days.append({'hours': hours, 'date': date(int(current_year), int(current_month), day), 'emp': teacher})
            else:
                if date(int(current_year), int(current_month), day) <= date(int(timezone.now().strftime('%Y')), int(current_month), int(current_day)):
                    att_got = EmployeeAttendance.objects.filter(
                            module_holder=module_holder,
                            employee_name=teacher,
                            date=date(int(current_year), int(current_month), day)
                    )
                    if att_got:
                        hours = EmployeeAttendance.objects.get(module_holder=module_holder, employee_name=teacher,date=date(int(current_year), int(current_month), day) )
                        t1 = datetime.strptime(hours.time_in, '%H:%M')
                        t2 = datetime.strptime(hours.time_out, '%H:%M')
                        t1 = datetime.strftime(t1, '%H:%M')
                        t2 = datetime.strftime(t2, '%H:%M')
                        hours = time_diff(t1, t2)
                        present_days.append({'hours': hours, 'date': date(int(current_year), int(current_month), day), 'emp': teacher})
                    else:
                        sun_or_other_day = 'a'
                else:
                    sun_or_other_day='n'
        net_salary = []
        for present_day in present_days:
            h = present_day['hours'].split(':')[0]
            m = present_day['hours'].split(':')[1]
            # print(h,':',m,'=============', teacher, '===============', hourly_rate.rate_per_hour, '=======', int(hourly_rate.rate_per_hour)*int(h))
            rate_per_minute = hourly_rate.rate_per_hour/60

            time = (int(h)*60)+int(m)
            print(teacher, time)
            salary = rate_per_minute*time
            net_salary.append(salary)
        # print(len(present_days),'=================LENGTH')
        # print('salary', sum(net_salary))

        salary_bonus = 0
        salary_other = 0
        salary_details = 'No Details'
        if salary_object:
            salary_bonus = salary_object.bonus
            salary_other = salary_object.other
            salary_details = salary_object.details

        employee_form_data.append(
           {'salaryform':SalaryForm(initial={
                'employee_name': Teacher.objects.get(pk=teacher.pk),
                'Salary_date': timezone.now().strftime('%Y-%m-%d'),
                'Salary_release_date': timezone.now().strftime('%Y-%m-%d'),
                'salary': int(sum(net_salary)),
                'advance_detected': monthly_detect, 
                'bonus': salary_bonus,
                # 'payment_method': 'Cash',
                'other': salary_other,
                'details': salary_details, 
            }),
            'status': status,
            'pk': teacher.pk,
            'salary_pk': salary_pk,
            'employee_name': teacher.username,
            'advance_taken': advance_taken,
            'advance_retured': advance_retured,
            'still_remaining': still_remaining
            }
        )
        
    context = {
        'current_month_redirect': timezone.now().strftime('%Y-%m-%d'),
        'employee_form_data': employee_form_data
    }
    return render(request, 'payroll/pay_salary.html', context)




# START SALARY DETAIL OF MONTHLY OF ALL TEACHERS
@login_required
@allowed_users('view_salary')
def salary_monthly_detail(request, date):
    search_form = FeeDefSerchForm()
    module_holder = request.user.username
    monthly_salary = []
    # if request.method=='GET':
    #     monthly_salary = Salary.objects.filter(
    #         Q(
    #             module_holder='masood',
    #             Salary_date__startswith=date.split('-')[:2]
    #         )
    #     )
    if request.method=='POST':
        monthly_salary = Salary.objects.filter(
            Q(
                module_holder=module_holder,
                Salary_date__startswith=request.POST.get('seacher_date')[:7]
            )
        )
    else:
        monthly_salary = Salary.objects.filter(
            Q(
                module_holder=module_holder,
                Salary_date__startswith=date[:7]
            )
        )

    print(monthly_salary)
    context = {
        'search_form': search_form,
        'monthly_salary':monthly_salary
    }
    return render(request,'payroll/salary_detail.html', context)


@login_required
@allowed_users('view_salary')
def salary_detail_one(request, pk, teacher_name_id):
    current_date_print = timezone.now().strftime('%B, %Y')
    current_year = timezone.now().strftime('%Y')
    current_month = timezone.now().strftime('%m')
    current_day = timezone.now().strftime('%d')
    module_holder = request.user.username
    if request.method=='POST':
        salary_object_base_id = Salary.objects.filter( #getting object base pk, from salary. slary saved before
                pk=request.POST.get('salary_pk'),
                employee_name=Teacher.objects.get(pk=request.POST.get('employee_name')),
                Salary_date__startswith=request.POST.get('Salary_date')[:7],
                module_holder=module_holder
            )
        salary_object = Salary.objects.filter(  #getting object base pk, from salary. salary is saving from here
                    employee_name=Teacher.objects.get(pk=request.POST.get('employee_name')),
                    Salary_date__startswith=request.POST.get('Salary_date')[:7],
                    module_holder=module_holder
                ).first()

        if len(salary_object_base_id): #getting object base pk, from salary. slary saved before
           
            updated_id = Salary.objects.filter(
                pk=request.POST.get('salary_pk'),
                employee_name=Teacher.objects.get(pk=request.POST.get('employee_name')),
                Salary_date__startswith=request.POST.get('Salary_date')[:7],
                module_holder=module_holder
            ).update(
                Salary_release_date=request.POST.get('Salary_release_date'),
                salary=request.POST.get('salary'),
                bonus=request.POST.get('bonus'),
                other=request.POST.get('other'),
                details=request.POST.get('details')
            )
            messages.success(request, 'it was submited before, Now it has been updated based ID!')
            return redirect('payroll:salary_detail_one', pk=pk, teacher_name_id=teacher_name_id)

        elif salary_object: #getting object base pk, from salary. salary is saving from here
            updated_id = Salary.objects.filter(
                employee_name=Teacher.objects.get(pk=request.POST.get('employee_name')),
                Salary_date__startswith=request.POST.get('Salary_date')[:7],
                module_holder=module_holder
            ).update(
                Salary_release_date=request.POST.get('Salary_release_date'),
                salary=request.POST.get('salary'),
                bonus=request.POST.get('bonus'),
                other=request.POST.get('other'),
                details=request.POST.get('details'),
                module_holder=module_holder
            )
            messages.success(request, 'it was submited before, Now it has been updated!')
            return redirect('payroll:salary_detail_one', pk=salary_object.pk, teacher_name_id=teacher_name_id)
        else:
            Salary(
                    employee_name=Teacher.objects.get(pk=request.POST.get('employee_name')),
                    Salary_date=request.POST.get('Salary_date'),
                    Salary_release_date=request.POST.get('Salary_release_date'),
                    salary=request.POST.get('salary'),
                    bonus=request.POST.get('bonus'),
                    other=request.POST.get('other'),
                    details=request.POST.get('details'),
                    module_holder=module_holder
            ).save()
        
            messages.success(request, 'Data has beed saved!')
            saved_id = Salary.objects.values('pk').filter().latest('pk')
            return redirect('payroll:salary_detail_one', pk=saved_id['pk'], teacher_name_id=teacher_name_id)
        
    # Making salary start here
    teacher = Teacher.objects.get(pk=teacher_name_id)
    salary_object = Salary.objects.filter(
                Q(employee_name=teacher,
                 Salary_date__startswith=timezone.now().strftime('%Y-%m'),
                 module_holder=module_holder
                 )
            ).first()
        
    status = 0
    if salary_object:
        salary_pk = salary_object.pk
        status = salary_object.salary
    else:
        salary_pk = 0
        status = 0
        
     

    advance_amount = AdvanceSalary.objects.values('advance_amount').filter(employee_name=teacher, module_holder=module_holder).aggregate(total_advance=Coalesce(Sum('advance_amount'), 0))
    detected_amount = Salary.objects.filter(employee_name=teacher, module_holder=module_holder).aggregate(detected_amount=Coalesce(Sum('advance_detected'),0))
        
    advance_taken = 0
    advance_retured = 0
    still_remaining = 0

    if int(advance_amount['total_advance']) > int(detected_amount['detected_amount']):
        advance_taken = advance_amount
        advance_retured = detected_amount
        still_remaining = int(advance_amount['total_advance'])-int(detected_amount['detected_amount'])

    monthly_detection = AdvanceSalary.objects.values('monthly_detection').filter(employee_name=teacher, module_holder=module_holder).aggregate(monthly_detection=Coalesce(Sum('monthly_detection'), 0))

    if still_remaining < int(monthly_detection['monthly_detection']):
        monthly_detect = still_remaining
    else:
        monthly_detect = int(monthly_detection['monthly_detection']) 

    # START WORKING WITH SALARY
    hourly_rate = Position.objects.get(pk=teacher.position_id, module_holder=module_holder)
    present_days = [] 
    sundays = []
    for sunday in get_all_says(int(current_year), int(current_month)):
        sundays.append(sunday.day)

    count_of_date_searched = int(current_year)+int(current_month)
    atte_status = []
    holidays = []
    leaves = []
    num_of_days = monthrange(int(current_year),int(current_month))[1]
    for day in range(1, num_of_days+1):
        try:
            hds = Leave.objects.values('from_date','to_date').filter(employee=teacher, type='h')
            for hd in hds:
                startdate = hd['from_date']
                enddate = hd['to_date']
                for days in daterange(startdate, enddate):
                    holidays.append(str(days.year)+'-'+str(convert_month(days.month))+'-'+str(convert_month(days.day)))
        except Exception as ex:
            holidays = []
            
        try:
            lvs = Leave.objects.values('from_date','to_date').filter(employee=teacher, type='l')
            for lv in lvs:
                startdate = lv['from_date']
                enddate = lv['to_date']
                for days in daterange(startdate, enddate):
                    leaves.append(str(days.year)+'-'+str(convert_month(days.month))+'-'+str(convert_month(days.day)))
        except Exception as ex:
            leaves = []

            
        heading = []
        count_of_date_searched =count_of_date_searched+1
        holiday_murging = str(current_year)+'-'+str(current_month)+'-'+str(convert_month(day))
            # print(holiday_murging,'===============================holuddd')
            
        sun_or_other_day = ''
        if day in sundays:
                # hours = Schedual.objects.get(module_holder=module_holder, pk=teacher.time_schedual.pk)
                # t1 = datetime.strptime(hours.time_in, '%H:%M')
                # t2 = datetime.strptime(hours.time_out, '%H:%M')
                # t1 = datetime.strftime(t1, '%H:%M')
                # t2 = datetime.strftime(t2, '%H:%M')
                # hours = time_diff(t1, t2)
                # present_days.append({'hours': hours, 'date': date(int(current_year), int(current_month), day), 'emp': teacher})
            sun_or_other_day = 's'
        elif holiday_murging in leaves:
            hours = Schedual.objects.get(module_holder=module_holder, pk=teacher.time_schedual.pk)
            t1 = datetime.strptime(hours.time_in, '%H:%M')
            t2 = datetime.strptime(hours.time_out, '%H:%M')
            t1 = datetime.strftime(t1, '%H:%M')
            t2 = datetime.strftime(t2, '%H:%M')
            hours = time_diff(t1, t2)
            present_days.append({'hours': hours, 'date': date(int(current_year), int(current_month), day), 'emp': teacher})

        elif holiday_murging in holidays:
            hours = Schedual.objects.get(module_holder=module_holder, pk=teacher.time_schedual.pk)
            t1 = datetime.strptime(hours.time_in, '%H:%M')
            t2 = datetime.strptime(hours.time_out, '%H:%M')
            t1 = datetime.strftime(t1, '%H:%M')
            t2 = datetime.strftime(t2, '%H:%M')
            hours = time_diff(t1, t2)
            present_days.append({'hours': hours, 'date': date(int(current_year), int(current_month), day), 'emp': teacher})
        else:
            if date(int(current_year), int(current_month), day) <= date(int(timezone.now().strftime('%Y')), int(current_month), int(current_day)):
                att_got = EmployeeAttendance.objects.filter(
                            module_holder=module_holder,
                            employee_name=teacher,
                            date=date(int(current_year), int(current_month), day)
                    )
                if att_got:
                    hours = EmployeeAttendance.objects.get(module_holder=module_holder, employee_name=teacher,date=date(int(current_year), int(current_month), day) )
                    t1 = datetime.strptime(hours.time_in, '%H:%M')
                    t2 = datetime.strptime(hours.time_out, '%H:%M')
                    t1 = datetime.strftime(t1, '%H:%M')
                    t2 = datetime.strftime(t2, '%H:%M')
                    hours = time_diff(t1, t2)
                    present_days.append({'hours': hours, 'date': date(int(current_year), int(current_month), day), 'emp': teacher})
                else:
                    sun_or_other_day = 'a'
            else:
                sun_or_other_day='n'
    net_salary = []
    for present_day in present_days:
        h = present_day['hours'].split(':')[0]
        m = present_day['hours'].split(':')[1]
        # print(h,':',m,'=============', teacher, '===============', hourly_rate.rate_per_hour, '=======', int(hourly_rate.rate_per_hour)*int(h))
        rate_per_minute = hourly_rate.rate_per_hour/60

        time = (int(h)*60)+int(m)
        salary = rate_per_minute*time
        net_salary.append(salary)
        # print(len(present_days),'=================LENGTH')
        # print('salary', sum(net_salary))

    salary_bonus = 0
    salary_other = 0
    salary_details = 'No Details'
    if salary_object:
        salary_bonus = salary_object.bonus
        salary_other = salary_object.other
        salary_details = salary_object.details
    # making salary  ends here

    salary_detail = Salary.objects.filter(employee_name=teacher, Salary_date__startswith=current_year+'-'+current_month).first()
    teacher_detail = Teacher.objects.get(username=teacher)

    total_year_salary_detail = Salary.objects.filter(
        Q(employee_name = teacher,
        Salary_date__startswith=timezone.now().strftime('%Y'),
        module_holder = module_holder
        )
    )
    
    total_bonus_other_salary = 0
    status = 0
    if salary_detail is not None:
        status = 1
        salary_form = SalaryForm(instance=salary_detail)
        total_bonus_other_salary = sum([salary_detail.salary, salary_detail.bonus, salary_detail.other])
    else:
        status = 0
        print('its comming in none')
        # salary_detail_values = False
        salary_form = SalaryForm(initial={
                    'employee_name': teacher,
                    'Salary_date': timezone.now().strftime('%Y-%m-%d'),
                    'Salary_release_date': timezone.now().strftime('%Y-%m-%d'),
                    'salary': int(sum(net_salary)),
                    'bonus': salary_bonus,
                    # 'payment_method': 'Cash',
                    'other': salary_other,
                    'details': salary_details,
                    
                })
    

    
    
    context = {
        'salary_pk':pk, 
        'salary_form': salary_form,
        'teacher_detail': teacher_detail,
        'salary_detail': salary_detail,
        'total_year_salary_detail': total_year_salary_detail,
        'current_date_print':current_date_print,
        'total_bonus_other_salary_in_word': num2words(total_bonus_other_salary),
        'status': status
    }
    return render(request, 'payroll/salary_detail_one.html', context)


# STRAT ADVANCE SALARY HERE
class AdvanceSalaryView(LoginRequiredMixin, ListView):
    # permission_required = 'academic.view_classes'
    model = AdvanceSalary
    login_url = 'home:login'
    # context_object_name = 'classes'
    template_name = 'payroll/advancesalary.html'
    success_message = 'Advance Salary has been created!'

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        context = super(AdvanceSalaryView, self).get_context_data(**kwargs)
        context['advancesalarys'] = AdvanceSalary.objects.filter(module_holder=module_holder)
        return context


class AdvanceSalaryCreate(LoginRequiredMixin , SuccessMessageMixin ,CreateView):
    # permission_required = 'academic.add_classes'
    success_message = 'Advance Salary has been created!'

    model = AdvanceSalary
    fields = [
        'employee_name',
        'advance_amount',
        'payment_date',
        'monthly_detection',
        'detail'
    ]
    login_url = 'home:lgoin'
    template_name = 'payroll/advancesalary_add.html'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.instance.module_holder = module_holder
        return super().form_valid(form)        

    def get_form(self, **kwargs):
        form = super(AdvanceSalaryCreate, self).get_form(**kwargs)
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.fields['payment_date'].widget.attrs = {'class': 'date'}
        form.fields['employee_name'].queryset = Teacher.objects.filter(module_holder=module_holder)
        form.fields['employee_name'].widget.attrs = {'class': 'basic-multiple'}
        return form

class AdvanceSalaryUpdate(LoginRequiredMixin, SuccessMessageMixin  ,UpdateView):
    # permission_required = 'academic.change_classes'
    model = AdvanceSalary
    fields = [
        'employee_name',
        'advance_amount',
        'payment_date',
        'monthly_detection',
        'detail'
    ]
    login_url = 'home:lgoin'
    template_name = 'payroll/advancesalary_add.html'
    success_message = 'Advance Salary has been updated!'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.instance.module_holder = module_holder
        return super().form_valid(form)


class AdvanceSalaryDelete(LoginRequiredMixin  ,DeleteView):
    login_url = 'home:lgoin'
    # permission_required = 'academic.delete_classes'
    model = AdvanceSalary
    success_url = reverse_lazy('payroll:advancesalary_view')