from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, TemplateView
from .models import Slider, StudentActivities, About, SchoolSummery,Gallery, NoticeBoard, ExtraCources, Events, RegisterNow, RegisteredStudent
from payroll.models import Teacher
from django.contrib.auth.mixins import PermissionRequiredMixin
from home.decorators import allowed_users
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from django.http import JsonResponse
import datetime
# Create your views here.

def websitesettinghome(request):
    return render(request, 'websitesetting/index.html')

class RegisteredStudentForm(forms.ModelForm):
    class Meta:
        model = RegisteredStudent
        fields = '__all__'


def registerstudent(request):
    rs = RegisterNow.objects.filter(pk__lt=2).first()
    rs = str(rs.end_date).split('-')
    form = RegisteredStudentForm(request.POST)
    if form.is_valid():
        if datetime.date(int(rs[0]), int(rs[1]), int(rs[2])) > datetime.date.today():
            form.save()
        else:
            return JsonResponse({'status': 'ok', 'message': 'Time has been finished. Try next time'})       
        return JsonResponse({'status': 'ok', 'message': 'Request has been Registered Successfully!'})
    else:
        return JsonResponse({'status': 'error', 'message': form.errors})

def register_request(request):
    registeredstudents = RegisteredStudent.objects.all()

    context = {
        'registeredstudents': registeredstudents
    }
    return render(request, 'websitesetting/registered_students_list.html', context)


class SliderCreate(SuccessMessageMixin, CreateView):
    model = Slider
    fields = ['header','detail','redirect_link','back_image']
    template_name = 'websitesetting/sliders.html'
    success_url = '/website_setting/sliders/'
    success_message = 'Slider Has Been Saved!'
    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder        
        
        
        form.instance.module_holder = module_holder
        form = super().form_valid(form)
        return form

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        context = super(SliderCreate, self).get_context_data(**kwargs)
        context['sliders'] = Slider.objects.filter(module_holder=module_holder)
        return context


class SliderUpdate(SuccessMessageMixin, UpdateView):
    model = Slider
    fields = ['header','detail','redirect_link','back_image']
    template_name = 'websitesetting/sliders.html'
    success_url = '/website_setting/sliders/'
    success_message = 'Slider has been updated!'
    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder  
        
        form.instance.module_holder = module_holder
        form = super().form_valid(form)
        return form

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        context = super(SliderUpdate, self).get_context_data(**kwargs)
        context['sliders'] = Slider.objects.filter(module_holder=module_holder)
        return context

class SliderDelete(SuccessMessageMixin, DeleteView):
    model = Slider
    success_message = 'Data has been deleted!'
    success_url = '/website_setting/sliders/'


# STUDENT ACTIVITIES
class StudentActivitiesCreate(SuccessMessageMixin, ListView):
    model = StudentActivities
    fields = ['name','image','description']
    template_name = 'websitesetting/studentactivities.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        context = super(StudentActivitiesCreate, self).get_context_data(**kwargs)
        context['studentsactivities'] = StudentActivities.objects.filter(module_holder=module_holder)
        return context

class StudentActivitiesUpdate(SuccessMessageMixin, UpdateView):
    model = StudentActivities
    fields = ['name','image','description']
    template_name = 'websitesetting/studentactivities_update.html'
    success_url = '/website_setting/studentactivities/'
    success_message = 'Student activity has been updated!'
    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder  
        
        form.instance.module_holder = module_holder
        form = super().form_valid(form)
        return form

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        context = super(StudentActivitiesUpdate, self).get_context_data(**kwargs)
        context['studentsactivities'] = StudentActivities.objects.filter(module_holder=module_holder)
        return context

# School details videos
class SchoolSummeryList(SuccessMessageMixin, ListView):
    model = SchoolSummery
    fields = ['heading','thumbnail','youtube_link','description']
    template_name = 'websitesetting/summery_list.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        context = super(SchoolSummeryList, self).get_context_data(**kwargs)
        context['schoolsummery'] = SchoolSummery.objects.filter(module_holder=module_holder)
        return context

class SchoolSummeryUpdate(SuccessMessageMixin, UpdateView):
    model = SchoolSummery
    fields = ['heading','thumbnail','youtube_link','description']
    template_name = 'websitesetting/summery_update.html'
    success_url = '/website_setting/summeryactivity/'
    success_message = 'Summery activity has been updated!'
    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder  
        
        form.instance.module_holder = module_holder
        form = super().form_valid(form)
        return form

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        context = super(SchoolSummeryUpdate, self).get_context_data(**kwargs)
        context['schoolsummery'] = SchoolSummery.objects.filter(module_holder=module_holder)
        return context


# School About
class AboutList(SuccessMessageMixin, ListView):
    model = About
    fields = ['about_heading','about_description','about_background']
    template_name = 'websitesetting/about.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        context = super(AboutList, self).get_context_data(**kwargs)
        context['about'] = About.objects.filter(module_holder=module_holder)
        return context

class AboutUpdate(SuccessMessageMixin, UpdateView):
    model = About
    fields = ['about_heading','about_description','about_background']
    template_name = 'websitesetting/about-edit.html'
    success_url = '/website_setting/about/'
    success_message = 'About has been updated!'
    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder  
        
        form.instance.module_holder = module_holder
        form = super().form_valid(form)
        return form

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        context = super(AboutUpdate, self).get_context_data(**kwargs)
        context['about'] = About.objects.filter(module_holder=module_holder)
        return context

# School details videos
class RegisterNowList(SuccessMessageMixin, ListView):
    model = RegisterNow
    fields = ['heading','end_date']
    template_name = 'websitesetting/registernow.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        context = super(RegisterNowList, self).get_context_data(**kwargs)
        context['registernow'] = RegisterNow.objects.filter(module_holder=module_holder)
        return context

class RegisterNowUpdate(SuccessMessageMixin, UpdateView):
    model = RegisterNow
    fields = ['heading','end_date']
    template_name = 'websitesetting/registernow_update.html'
    success_url = '/website_setting/registernow/'
    success_message = '(Register Now) has been updated!'
    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder  
        
        form.instance.module_holder = module_holder
        form = super().form_valid(form)
        return form

    def get_form(self, **kwargs):
        form = super(RegisterNowUpdate, self).get_form(**kwargs)
        form.fields['end_date'] = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
        return form

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        context = super(RegisterNowUpdate, self).get_context_data(**kwargs)
        context['registernow'] = RegisterNow.objects.filter(module_holder=module_holder)
        return context
    
# Extra Cources Details
class ExtraCourcesCreate(SuccessMessageMixin, CreateView):
    model = ExtraCources
    fields = ['name','image','price','faculty','description']
    template_name = 'websitesetting/extra_cources.html'
    success_url = '/website_setting/extracources/'
    success_message = 'Extra Course Has Been Saved!'
    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder        
        
        
        form.instance.module_holder = module_holder
        form = super().form_valid(form)
        return form

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        context = super(ExtraCourcesCreate, self).get_context_data(**kwargs)
        context['extracources'] = ExtraCources.objects.filter(module_holder=module_holder)
        return context


class ExtraCourcesUpdate(SuccessMessageMixin, UpdateView):
    model = ExtraCources
    fields = ['name','image','price','faculty','description']
    template_name = 'websitesetting/extra_cources.html'
    success_url = '/website_setting/extracources/'
    success_message = 'Extra Course has been updated!'
    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder  
        
        form.instance.module_holder = module_holder
        form = super().form_valid(form)
        return form

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        context = super(ExtraCourcesUpdate, self).get_context_data(**kwargs)
        context['extracources'] = ExtraCources.objects.filter(module_holder=module_holder)
        return context

class ExtraCourcesDelete(SuccessMessageMixin, DeleteView):
    model = ExtraCources
    success_message = 'Extra Course has been deleted!'
    success_url = '/website_setting/extracources/'


# Extra Gallery
class GalleryCreate(SuccessMessageMixin, CreateView):
    model = Gallery
    fields = ['heading','image']
    template_name = 'websitesetting/gallery.html'
    success_url = '/website_setting/gallery/'
    success_message = 'Image Has Been Saved!'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder  
        
        form.instance.module_holder = module_holder
        form = super().form_valid(form)
        return form
    
    def form_invalid(self, form):
        form = super().form_invalid(form)
        return form

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        context = super(GalleryCreate, self).get_context_data(**kwargs)
        context['gallery'] = Gallery.objects.filter(module_holder=module_holder)
        return context


class GalleryUpdate(SuccessMessageMixin, UpdateView):
    model = Gallery
    fields = ['heading','image']
    template_name = 'websitesetting/gallery.html'
    success_url = '/website_setting/gallery/'
    success_message = 'Image has been updated!'
    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder  
        
        form.instance.module_holder = module_holder
        form = super().form_valid(form)
        return form

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        context = super(GalleryUpdate, self).get_context_data(**kwargs)
        context['gallery'] = Gallery.objects.filter(module_holder=module_holder)
        return context

class GalleryDelete(SuccessMessageMixin, DeleteView):
    model = Gallery
    success_message = 'Image has been deleted!'
    success_url = '/website_setting/gallery/'


# Extra Gallery
class NoticeBoardCreate(SuccessMessageMixin, CreateView):
    model = NoticeBoard
    fields = ['heading','date','description']
    template_name = 'websitesetting/notice_board.html'
    success_url = '/website_setting/noticeboard/'
    success_message = 'Notice Has Been Saved!'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder  
        
        form.instance.module_holder = module_holder
        form = super().form_valid(form)
        return form

    def get_form(self, **kwargs):
        form = super(NoticeBoardCreate, self).get_form(**kwargs)
        form.fields['date'] = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
        return form

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        context = super(NoticeBoardCreate, self).get_context_data(**kwargs)
        context['noticeboard'] = NoticeBoard.objects.filter(module_holder=module_holder)
        return context


class NoticeBoardUpdate(SuccessMessageMixin, UpdateView):
    model = NoticeBoard
    fields = ['heading','date','description']
    template_name = 'websitesetting/notice_board.html'
    success_url = '/website_setting/noticeboard/'
    success_message = 'Notice has been updated!'
    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder  
        
        form.instance.module_holder = module_holder
        form = super().form_valid(form)
        return form

    def get_form(self, **kwargs):
        form = super(NoticeBoardUpdate, self).get_form(**kwargs)
        form.fields['date'] = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
        return form

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        context = super(NoticeBoardUpdate, self).get_context_data(**kwargs)
        context['noticeboard'] = NoticeBoard.objects.filter(module_holder=module_holder)
        return context

class NoticeBoardDelete(SuccessMessageMixin, DeleteView):
    model = NoticeBoard
    success_message = 'Notice has been deleted!'
    success_url = '/website_setting/noticeboard/'

# Extra Cources Details
class EventsCreate(SuccessMessageMixin, CreateView):
    model = Events
    fields = ['name','image','heading','event_date','start_time','end_time','city','description']
    template_name = 'websitesetting/events.html'
    success_url = '/website_setting/events/'
    success_message = 'Events Has Been Saved!'
    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder  
        form.instance.module_holder = module_holder
        form = super().form_valid(form)
        return form

    def get_form(self, **kwargs):
        form = super(EventsCreate, self).get_form(**kwargs)
        form.fields['event_date'] = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
        form.fields['start_time'] = forms.CharField(widget=forms.TextInput(attrs={'type': 'time'}))
        form.fields['end_time'] = forms.CharField(widget=forms.TextInput(attrs={'type': 'time'}))
        return form

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        context = super(EventsCreate, self).get_context_data(**kwargs)
        context['events'] = Events.objects.filter(module_holder=module_holder)
        return context


class EventsUpdate(SuccessMessageMixin, UpdateView):
    model = Events
    fields = ['name','image','heading','event_date','start_time','end_time','city','description']
    template_name = 'websitesetting/events.html'
    success_url = '/website_setting/events/'
    success_message = 'Events has been updated!'
    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder  
        
        form.instance.module_holder = module_holder
        form = super().form_valid(form)
        return form

    def get_form(self, **kwargs):
        form = super(EventsUpdate, self).get_form(**kwargs)
        form.fields['event_date'] = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
        form.fields['start_time'] = forms.CharField(widget=forms.TextInput(attrs={'type': 'time'}))
        form.fields['end_time'] = forms.CharField(widget=forms.TextInput(attrs={'type': 'time'}))
        return form
    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        context = super(EventsUpdate, self).get_context_data(**kwargs)
        context['events'] = Events.objects.filter(module_holder=module_holder)
        return context

class EventsDelete(SuccessMessageMixin, DeleteView):
    model = Events
    success_message = 'Events has been deleted!'
    success_url = '/website_setting/events/'