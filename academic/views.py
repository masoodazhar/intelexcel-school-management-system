from django.shortcuts import render, redirect
from django.views.generic import  CreateView, UpdateView, DeleteView, ListView, TemplateView
from django.views.generic.edit import BaseCreateView
from .models import Classes, Subject, Routine, Section, Room
from payroll.models import Teacher
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django import forms
from django.contrib.auth.models import User, Permission, Group
# from payroll.forms import TeacherForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from home.decorators import allowed_users
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .forms import SubjectForm, SectionForm, ClassesForm
from home.models import Setting, SchoolProfile
from datetime import datetime, time, date, timedelta

# Create your views here.

def time_diff(time_str1, time_str2):
    t1 = datetime.strptime(time_str1, '%H:%M')
    t2 = datetime.strptime(time_str2, '%H:%M')
    dt = abs(t2 - t1)
    return time(dt.seconds // 3600, (dt.seconds // 60) % 60).strftime('%H:%M')

def get_section_by_class(request):
    class_id = request.GET.get('class_name')
    section_from_class = Classes.objects.get(pk=class_id)
    print(section_from_class.section.pk)
    sections = Section.objects.get(pk=section_from_class.section.pk)
    section = [{
        'id': sections.pk,
        'name': sections.section_name
    }]
    return JsonResponse({'data': section})

# @allowed_users('view_academic')
@login_required
def AcademicView(request):
    if request.user.is_staff:
        module_holder = request.user.username
    else:
        this_holder = Teacher.objects.get(user_ptr_id=request.user.id)
        module_holder = this_holder.module_holder
    
    total_teachers = Teacher.objects.filter(module_holder=module_holder).count()
    teachers = Teacher.objects.filter(module_holder=module_holder)
    total_subject = Subject.objects.filter(module_holder=module_holder).count()
    subjects = Subject.objects.filter(module_holder=module_holder)
    total_class = Classes.objects.filter(module_holder=module_holder).count()
    classes = Classes.objects.filter(module_holder=module_holder)
    total_routine = Routine.objects.filter(module_holder=module_holder).count()
    routines = Routine.objects.filter(module_holder=module_holder)

    all_data = {
        'total_teachers': total_teachers,
        'total_subject': total_subject,
        'total_class': total_class,
        'total_routine': total_routine,
        'teachers': teachers,
        'subjects': subjects,
        'classes': classes,
        'routines': routines,
    }

    return render(request, 'academic/academic_main.html', all_data)
  


# STRAT CLASSES HERE
class RoomView(LoginRequiredMixin, ListView):
    # permission_required = 'academic.view_room'
    model = Room
    login_url = 'home:login'
    # context_object_name = 'classes'
    template_name = 'academic/room.html'
    success_message = 'Room has been created!'

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        context = super(RoomView, self).get_context_data(**kwargs)
        context['room'] = Room.objects.filter(module_holder=module_holder)
        return context


class RoomCreate(LoginRequiredMixin , SuccessMessageMixin ,CreateView):
    # permission_required = 'academic.add_room'
    success_message = 'Room has been created!'

    model = Room
    fields = [
        'room_name',
        'room_number',
    ]
    login_url = 'home:lgoin'
    template_name = 'academic/room_add.html'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
      
        form.instance.module_holder = module_holder
        return super().form_valid(form)        


class RoomUpdate(LoginRequiredMixin, SuccessMessageMixin  ,UpdateView):
    # permission_required = 'academic.change_room'
    model = Room
    fields = [
        'room_name',
        'room_number',
    ]
    login_url = 'home:lgoin'
    template_name = 'academic/room_add.html'
    success_message = 'Room has been updated!'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.instance.module_holder = module_holder
        return super().form_valid(form)


class RoomDelete(LoginRequiredMixin  ,DeleteView):
    login_url = 'home:lgoin'
    # permission_required = 'academic.delete_room'
    model = Room
    success_url = reverse_lazy('academic:room_view')



# STRAT CLASSES HERE
class ClassesView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'academic.view_classes'
    model = Classes
    login_url = 'home:login'
    # context_object_name = 'classes'
    template_name = 'academic/classes.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        context = super(ClassesView, self).get_context_data(**kwargs)
        context['classes'] = Classes.objects.filter(module_holder=module_holder)
        return context


class ClassesCreate(LoginRequiredMixin ,PermissionRequiredMixin, SuccessMessageMixin ,CreateView):
    permission_required = 'academic.add_classes'
    success_message = 'Class has been created!'

    model = Classes
    fields = [
        'class_name',
        'class_number',
        'fee',
        'section',
        'discount',
        'note'
    ]
    sectionform = SectionForm()
    login_url = 'home:lgoin'
    template_name = 'academic/classes_add.html'

    def get_form(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form = super(ClassesCreate, self).get_form(**kwargs)
        form.fields['section'].widget.attrs = {'class': 'basic-multiple', 'autocomplete': 'off'}
        form.fields['section'].queryset = Section.objects.filter(module_holder=module_holder)
        
        return form
    def get_context_data(self, **kwargs):
        context = super(ClassesCreate, self).get_context_data(**kwargs)
        context['sectionform'] = self.sectionform
        return context

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.instance.module_holder = module_holder
        resolver = super().form_valid(form)        
        if self.request.is_ajax():
            classes = Classes.objects.filter(module_holder=module_holder).order_by('-id').first()
            data = {
                'pk': classes.pk,
                'name': classes.class_name,
                'monthly_fee': classes.fee,
                'discount': classes.discount,
                'status': 'success'
            }
            return JsonResponse(data)
        else:
            return resolver


class ClassesUpdate(LoginRequiredMixin, SuccessMessageMixin ,PermissionRequiredMixin ,UpdateView):
    permission_required = 'academic.change_classes'
    model = Classes
    fields = [
       'class_name',
        'class_number',
        'fee',
        'section',
        'discount',
        'note'
    ]
    login_url = 'home:lgoin'
    template_name = 'academic/classes_add.html'
    success_message = 'Class has been updated!'

    def get_form(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form = super(ClassesUpdate, self).get_form(**kwargs)
        form.fields['section'].widget.attrs = {'class': 'basic-multiple', 'autocomplete': 'off'}
        form.fields['section'].queryset = Section.objects.filter(module_holder=module_holder)
        print(module_holder)
        return form

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.instance.module_holder = module_holder
        return super().form_valid(form)


class ClassesDelete(LoginRequiredMixin ,PermissionRequiredMixin ,DeleteView):
    login_url = 'home:lgoin'
    permission_required = 'academic.delete_classes'
    model = Classes
    success_url = reverse_lazy('academic:classes_view')


# SECTION START HERE
class SectionCreate( LoginRequiredMixin,PermissionRequiredMixin ,SuccessMessageMixin, CreateView):
    permission_required = 'academic.add_section'
    template_name = 'academic/section_view_or_create.html'
    model = Section
    login_url = 'home:lgoin'
    fields = ['section_name']
    success_message = 'Section has been created successfully!'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        form.instance.module_holder = module_holder
        response = super().form_valid(form)
        if self.request.is_ajax():          
            last = Section.objects.filter(module_holder=module_holder).order_by('-id').first()
            data = {
                'pk': last.pk,
                'name': last.section_name,
                'status': 'success'
            }           
            return JsonResponse(data)
        else:
            return response
            # return super().form_valid(form)
        
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({'status': 'already'})
        return response

    def get_context_data(self, **kwargs):
        context = super(SectionCreate, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        context['section'] = Section.objects.filter(module_holder=module_holder)
       
        return context


class SectionUpdate(LoginRequiredMixin, SuccessMessageMixin ,PermissionRequiredMixin ,UpdateView):
    permission_required = 'academic.change_section'
    template_name = 'academic/section_view_or_create.html'
    model = Section
    login_url = 'home:lgoin'
    fields = ['section_name']
    success_message = 'Section has been updated!'

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


class SectionDelete(PermissionRequiredMixin, LoginRequiredMixin  ,DeleteView):
    permission_required = 'academic.delete_section'
    login_url = 'home:lgoin'
    model = Section
    success_url = reverse_lazy('student:create_section')


# STRAT SUBJECT HERE
class SubjectView(PermissionRequiredMixin, LoginRequiredMixin ,ListView):
    permission_required = 'academic.view_subject'
    model = Subject
    login_url = 'home:lgoin'
    template_name = 'academic/subject.html'
    

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        context = super(SubjectView, self).get_context_data(**kwargs)
        subject_data = Subject.objects.filter(module_holder=module_holder)
        


        all_subject_row = []
        for sd in subject_data:
            class_names = []
            class_name_ids = sd.class_name.replace('[','').replace(']','').split(',')
            for class_id in class_name_ids:
                clss = Classes.objects.filter(pk=class_id).first()
                class_names.append(
                    {'class_name': clss.class_name}
                )

            all_subject_row.append({
                'subject_name': sd.subject_name,
                'pk': sd.pk,
                'subject_code': sd.subject_code,
                'note': sd.note,
                'class_name': class_names
            })
                
        context['subjects'] = all_subject_row
        return context
        

class SubjectCreate(PermissionRequiredMixin, SuccessMessageMixin, LoginRequiredMixin ,CreateView):
    permission_required = 'academic.add_subject'
    model = Subject
    login_url = 'home:lgoin'
    fields = [
        'class_name',
        # 'teacher_name',
        'subject_type',
        'pass_mark',
        'final_mark',
        'subject_name',
        'subject_code',
        'note'
    ]

    template_name = 'academic/subject_add.html'
    success_message = 'Subject has been Created!'

    def form_valid(self, form):        
        if self.request.user.is_staff:
            module_holder = self.request.user.username
            form.instance.module_holder = module_holder
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            form.instance.module_holder = this_holder.module_holder

        class_list = []
        t = self.request.POST.getlist('class_name')
        for i in t:
            class_list.append(int(i))

        form.instance.class_name = class_list
        resolver = super().form_valid(form)       
        return resolver

    def get_form(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form = super(SubjectCreate, self).get_form(**kwargs)
        form.fields['subject_type'].widget.attrs = {'class': 'basic-multiple'}
        form.fields['class_name'] = forms.ModelChoiceField(queryset = Classes.objects.filter(module_holder=module_holder))
        form.fields['class_name'].widget.attrs = {'class': 'basic-multiple', 'multiple': 'multiple', 'autocomplete': 'off'}
        form.fields['class_name'].queryset = Classes.objects.filter(module_holder=module_holder)
        print(module_holder)
        return form

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        context = super(SubjectCreate, self).get_context_data(**kwargs)
        context['classesform'] = ClassesForm(module_holder)
        return context

    

class SubjectUpdate(PermissionRequiredMixin, SuccessMessageMixin, LoginRequiredMixin ,UpdateView):
    permission_required = 'academic.change_subject'
    model = Subject
    login_url = 'home:lgoin'
    fields = [
        'class_name',
        # 'teacher_name',
        'subject_type',
        'pass_mark',
        'final_mark',
        'subject_name',
        'subject_code',
        'note'
    ]
    template_name = 'academic/subject_add.html'
    success_message = 'Subject has been Updated!'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
            form.instance.module_holder = module_holder
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            form.instance.module_holder = this_holder.module_holder
        class_list = []
        t = self.request.POST.getlist('class_name')
        for i in t:
            class_list.append(int(i))
        form.instance.class_name = class_list
        return super().form_valid(form)

    def get_form(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form = super(SubjectUpdate, self).get_form(**kwargs)
        form.fields['subject_type'].widget.attrs = {'class': 'basic-multiple'}
        form.fields['class_name'] = forms.ModelChoiceField(queryset = Classes.objects.filter(module_holder=module_holder))
        form.fields['class_name'].widget.attrs = {'class': 'basic-multiple', 'multiple': 'multiple', 'autocomplete': 'off'}
        form.fields['class_name'].queryset = Classes.objects.filter(module_holder=module_holder)
        return form

class SubjectDelete(PermissionRequiredMixin, LoginRequiredMixin ,DeleteView):
    permission_required = 'academic.delete_subject'
    model = Subject
    login_url = 'home:lgoin'
    success_url = reverse_lazy('academic:subject_view')


# STRAT ROUTINE HERE
class RoutineView(PermissionRequiredMixin, LoginRequiredMixin ,ListView):
    permission_required = 'academic.view_routine'
    model = Routine
    login_url = 'home:lgoin'
    template_name = 'academic/routine.html'
    
    def get_context_data(self, **kwargs):
        context = super(RoutineView, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        context['routines'] = Routine.objects.filter(module_holder=module_holder)
        return context
    

class RoutineCreate(PermissionRequiredMixin, SuccessMessageMixin, LoginRequiredMixin ,CreateView):
    permission_required = 'academic.add_routine'
    model = Routine
    login_url = 'home:lgoin'
    fields = [
        'date_from',
        'date_to',
        'class_name',
        'section_name',
        'subject_name',
        'school_day',
        'teacher_name',
        'start_time',
        'end_time',
        'room'
    ]
    template_name = 'academic/routine_add.html'
    success_message = 'Routine has been Created!'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.instance.module_holder = module_holder        
        return super().form_valid(form)        
    
    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        
        context = super(RoutineCreate, self).get_context_data(**kwargs)
        context['setting_time'] = SchoolProfile.objects.filter(module_holder=module_holder).first()
        setting = SchoolProfile.objects.filter(module_holder=module_holder).first()
        t1 = datetime.strptime(setting.school_timing_from, '%H:%M')
        t2 = datetime.strptime(setting.school_timing_to, '%H:%M')
        t1 = datetime.strftime(t1, '%H:%M')
        t2 = datetime.strftime(t2, '%H:%M')
        hours = time_diff(t1, t2)
        hourssplited = hours.split(':')
        hours_minuts = int(hourssplited[0])*60
        hours_minuts = hours_minuts+int(hourssplited[1])
        context['times'] = hours_minuts    
        context['classesform'] = ClassesForm(module_holder)
        context['sectionform']  = SectionForm()
        return context

    def get_form(self, **kwargs):
        form = super(RoutineCreate, self).get_form(**kwargs)
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        setting = SchoolProfile.objects.filter(module_holder=module_holder).first()
        
        
        # form['start_time'] = setting.school_timing_from
        # form['end_time'] = setting.school_timing_to
        form.fields['start_time'].widget = forms.TextInput( attrs = {'type': 'time', 'value': setting.school_timing_from})
        form.fields['end_time'].widget = forms.TextInput( attrs = {'type': 'time', 'value': setting.school_timing_to})
        form.fields['date_from'].widget=forms.TextInput(attrs = {'type': 'date'})
        form.fields['date_to'].widget= forms.TextInput(attrs = {'type': 'date'})
        # form.fields['school_day'].widget.attrs = {'class': 'basic-multiple'}
        FAVORITE_COLORS_CHOICES = [ ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'),('Saturday', 'Saturday'),('Sunday', 'Sunday'), ]
        form.fields['school_day'] = forms.TypedMultipleChoiceField(choices=FAVORITE_COLORS_CHOICES,widget=forms.CheckboxSelectMultiple)
        form.fields['class_name'].widget.attrs = {'class': 'basic-multiple'}
        form.fields['class_name'].queryset = Classes.objects.filter(module_holder=module_holder)
        form.fields['section_name'].widget.attrs = {'class': 'basic-multiple'}
        form.fields['section_name'].queryset = Section.objects.filter(module_holder=module_holder)
        
        form.fields['room'].widget.attrs = {'class': 'basic-multiple'}
        form.fields['room'].queryset = Room.objects.filter(module_holder=module_holder)

        form.fields['subject_name'].widget.attrs = {'class': 'basic-multiple'}
        form.fields['subject_name'].queryset = Subject.objects.filter(module_holder=module_holder)
        form.fields['teacher_name'].widget.attrs = {'class': 'basic-multiple'}
        form.fields['teacher_name'].queryset = Teacher.objects.filter(module_holder=module_holder)
        return form


class RoutineUpdate(PermissionRequiredMixin, SuccessMessageMixin, LoginRequiredMixin ,UpdateView):
    permission_required = 'academic.change_routine'
    model = Routine
    login_url = 'home:lgoin'
    fields = [
        'date_from',
        'date_to',
        'class_name',
        'section_name',
        'subject_name',
        'school_day',
        'teacher_name',
        'start_time',
        'end_time',
        'room'
    ]
    template_name = 'academic/routine_add.html'
    success_message = 'Routine has been updated'    

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.instance.module_holder = module_holder
        return super().form_valid(form)
    
    def get_form(self, **kwargs):
        form = super(RoutineUpdate, self).get_form(**kwargs)
        form.fields['start_time'].widget = forms.TextInput( attrs = {'type': 'time'})
        form.fields['end_time'].widget = forms.TextInput( attrs = {'type': 'time'})
        return form
    
    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        
        context = super(RoutineUpdate, self).get_context_data(**kwargs)
        context['setting_time'] = SchoolProfile.objects.filter(module_holder=module_holder).first()
        setting = SchoolProfile.objects.filter(module_holder=module_holder).first()
        t1 = datetime.strptime(setting.school_timing_from, '%H:%M')
        t2 = datetime.strptime(setting.school_timing_to, '%H:%M')
        t1 = datetime.strftime(t1, '%H:%M')
        t2 = datetime.strftime(t2, '%H:%M')
        hours = time_diff(t1, t2)
        hourssplited = hours.split(':')
        hours_minuts = int(hourssplited[0])*60
        hours_minuts = hours_minuts+int(hourssplited[1])
        context['times'] = hours_minuts    
        context['classesform'] = ClassesForm(module_holder)
        context['sectionform']  = SectionForm()
        return context

    def get_form(self, **kwargs):
        form = super(RoutineUpdate, self).get_form(**kwargs)
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        setting = SchoolProfile.objects.filter(module_holder=module_holder).first()
        
        
        # form['start_time'] = setting.school_timing_from
        # form['end_time'] = setting.school_timing_to
        form.fields['start_time'].widget = forms.TextInput( attrs = {'type': 'time', 'value': setting.school_timing_from})
        form.fields['end_time'].widget = forms.TextInput( attrs = {'type': 'time', 'value': setting.school_timing_to})
        form.fields['date_from'].widget=forms.TextInput(attrs = {'type': 'date'})
        form.fields['date_to'].widget= forms.TextInput(attrs = {'type': 'date'})
        # form.fields['school_day'].widget.attrs = {'class': 'basic-multiple'}
        FAVORITE_COLORS_CHOICES = [ ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'),('Saturday', 'Saturday'),('Sunday', 'Sunday'), ]
        form.fields['school_day'] = forms.TypedMultipleChoiceField(choices=FAVORITE_COLORS_CHOICES,widget=forms.CheckboxSelectMultiple)
        form.fields['class_name'].widget.attrs = {'class': 'basic-multiple'}
        form.fields['class_name'].queryset = Classes.objects.filter(module_holder=module_holder)
        form.fields['section_name'].widget.attrs = {'class': 'basic-multiple'}
        form.fields['section_name'].queryset = Section.objects.filter(module_holder=module_holder)
        
        form.fields['room'].widget.attrs = {'class': 'basic-multiple'}
        form.fields['room'].queryset = Room.objects.filter(module_holder=module_holder)

        form.fields['subject_name'].widget.attrs = {'class': 'basic-multiple'}
        form.fields['subject_name'].queryset = Subject.objects.filter(module_holder=module_holder)
        form.fields['teacher_name'].widget.attrs = {'class': 'basic-multiple'}
        form.fields['teacher_name'].queryset = Teacher.objects.filter(module_holder=module_holder)
        return form


class RoutineDelete(PermissionRequiredMixin, LoginRequiredMixin ,DeleteView):
    permission_required = 'academic.delete_routine'
    login_url = 'home:lgoin'
    model = Routine
    success_url = reverse_lazy('academic:routine_view')

