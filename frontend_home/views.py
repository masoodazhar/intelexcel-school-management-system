from django.shortcuts import render
from django.views.generic import TemplateView
from student.models import Admission
from django.contrib.auth.hashers import make_password
import json
from websitesetting.models import Slider, StudentActivities, SchoolSummery, ExtraCources, Events, RegisterNow,About, ExtraCources,NoticeBoard, Gallery
from django.shortcuts import redirect
from payroll.models import Teacher
from django.http import HttpResponse
from django.utils import timezone
# from django.contrib.auth.hashers import make_password
# Create your views here.

def FrontEndHome(request):
    sliders = Slider.objects.all()
    if not sliders:
        headings = ['Heading 1', 'Heading 2']
        for heading in headings:
            slider = Slider(
                header = heading,
                back_image = 'No-Image-Found.png',
                detail = 'No Details',
                module_holder = 'admin',
                redirect_link='#'
            )
            slider.save()


    studentactivities = StudentActivities.objects.all()
    if not studentactivities:
        names = ['Feeding', 'Payling','Caring','Learning']
        for name in names:
            std = StudentActivities(
                name = name,
                image = 'No-Image-Found.png',
                description = 'No Description',
                module_holder = 'admin'
            )
            std.save()
        
        
    schoolsummery = SchoolSummery.objects.all()

    if not schoolsummery:
        ss = SchoolSummery(
            heading = 'No Heading. manage from dashboard',
            thumbnail = 'No-Image-Found.png',
            youtube_link = '#',
            description = 'No Description, manage from dashboard',
            module_holder = 'admin'
        )
        ss.save()

    extracources = ExtraCources.objects.all()
    # if not extracources:
    #     ec = ExtraCources(
    #         name = 'No Heading. manage from dashboard',
    #         description = 'No Description, manage from dashboard',
    #         image = 'No-Image-Found.png',
    #         price = 0,
    #         faculty = 1,
    #         module_holder = 'admin'
    #     )
    #     ec.save()
    events = Events.objects.filter()
    # if not Events:
    #     ec = ExtraCources(
    #         name = 'Need a name. manage from dashboard',
    #         image = 'No-Image-Found.png',
    #         heading = 'No Heading. manage from dashboard',
    #         event_date
    #         start_time
    #         end_time
    #         city
    #         description = 'No Description, manage from dashboard',
            
    #         price = 0,
    #         faculty = 1,
    #         module_holder = 'admin'
    #     )
    # ec.save()
    registernow = RegisterNow.objects.all().first()
    if not registernow:
        reg = RegisterNow(
            heading = 'New Technology Cource',
            end_date = timezone.now().strftime('%Y-%m-%d'),
            module_holder = 'admin'
        )   
        reg.save()  
        return redirect('/frontend/')   
    register_now_end_date = registernow.end_date
    register_now_end_date = register_now_end_date.strftime('%Y/%m/%d')
    teachers = Teacher.objects.all()
    # print('asdsadasd=========',register_now_end_date.strftime('%y/%m/%d'))
    context = {
        'sliders': sliders,
        'studentactivities': studentactivities,
        'schoolsummery': schoolsummery,
        'extracources': extracources,
        'events': events,
        'registernow': registernow,
        'register_now_end_date': register_now_end_date,
        'teachers': teachers
    }
    template_name = 'frontend/index.html'
    return render(request, template_name, context)
   

def FrontEndAbout(request):
    about = About.objects.all().first()
    if not about:
        reg = About(
            about_heading = 'No Heading. Manage from dashboard.',
            about_description = 'No Description. Manage from dashboard.',
            about_background = 'No-Image-Found.png',
            module_holder = 'admin'
        )   
        reg.save()  
        return redirect('/frontend/frontendabout/') 
    template_name = 'frontend/about.html'
    teachers = Teacher.objects.all()

    return render(request, template_name, {'about': about, 'teachers': teachers})

def FrontEndCources(request):
    cources = ExtraCources.objects.all()
    template_name = 'frontend/courses-grid.html'
    return render(request, template_name, {'cources': cources})
    

def FrontEndEvent(request):
    events = Events.objects.all()

    template_name = 'frontend/event-layout.html'
    return render(request, template_name, {'events': events})

def FrontEndGallery(request):
    template_name = 'frontend/gallery.html'
    galleries = Gallery.objects.all()
    return render(request,template_name, {'galleries': galleries})

def FrontEndContact(request):
    template_name = 'frontend/contact.html'
    
    return render(request, template_name)

def NoticBoard(request):
    template_name = 'frontend/notic_board.html'
    notices = NoticeBoard.objects.all()
    return render(request, template_name, {'notices': notices})



class FrontEndLogin(TemplateView):
    template_name = 'frontend/login.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        student_login = False
        request.session['student_login'] = False
        invalid_login_message = '' 
        login_data = {}
        try:
            data = Admission.objects.get(Student_email_address = request.POST.get('email'), password=request.POST.get('password'))
            login_data.update({'name_of_student': data.name_of_student})
            login_data.update({'admission_registration': data.admission_registration})
            login_data.update({'father_name': data.father_name})
            login_data.update({'father_cnic': data.father_cnic})
            login_data.update({'cast': data.cast})
            login_data.update({'father_profession': data.father_profession})
            login_data.update({'date_of_birth': str(data.date_of_birth)})
            login_data.update({'contact': data.contact})
            login_data.update({'address': data.address})
            login_data.update({'gender': data.gender})
            login_data.update({'monthly_tution_fee': data.monthly_tution_fee})
            login_data.update({'student_email_address': data.Student_email_address})
            login_data.update({'photo': data.photo.url})
            login_data.update({'admission_date': str(data.admission_date)})            
            request.session['student_login'] = True  
            request.session['student_id'] = data.pk  
            request.session['student_photo'] = data.photo.url 
            request.session['student_name'] = data.name_of_student
            student_login = True         
            return redirect('frontendhome')
        except Exception as identifier:
            print(identifier)
            student_login = False
            request.session['student_login'] = False        
            invalid_login_message = "Please enter a correct username and password. Note that both fields may be case-sensitive."
        context = {
            'student_login': student_login,
            'login_data': login_data,
            'invalid_login_message': invalid_login_message
        }
        return render(request, self.template_name, context)
    

class FrontEndRegister(TemplateView):
    template_name = 'frontend/register.html'

def FrontEndLogout(request):
    request.session['student_login'] = False
    request.session['student_id'] = False
    return redirect('frontendhome')

def emptypage(request):
    return render(request, 'frontend/emptypage.html')