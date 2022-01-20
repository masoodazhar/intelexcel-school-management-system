from django.db import models
from django.utils import timezone
from payroll.models import Teacher

# Create your models here.

class MainSetting(models.Model):
    school_email = models.EmailField(default='info@intelexcel.com')
    contact_number = models.CharField(max_length=20, default='03242806949')
    logo = models.ImageField(upload_to='schooldata', default='intelexcel.png')
    Short_descrption = models.TextField('SHort Description will display in footer', default='This is a service provider based educational system. trying to fill all of empty spaces in education system. need your suggestion. for any query please contact info@intelexcel.com')
    full_address = models.TextField()
    twitter = models.CharField(max_length=255, default='https://twitter.com/intelexcel')
    linkedin = models.CharField(max_length=255, default='https://linkedin.com/intel3xcel')
    facebook = models.CharField(max_length=255, default='https://facebook.com/intelexcel')
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'mainsetting'
    
    def __str__(self):
        return self.school_email


class Slider(models.Model):
    header = models.CharField(max_length=50)
    detail = models.TextField()
    back_image = models.ImageField('Slider Back Image (2014x456) size recommended',upload_to='frontend_sliders', default='defaultslider.jpg')
    redirect_link = models.CharField(max_length=150, default="#")
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'slider'
    
    def __str__(self):
        return self.header 

class StudentActivities(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='frontend_activities', default='default.jpg')
    description = models.TextField()
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'studentactivities'

    def __str__(self):
        return self.name

class SchoolSummery(models.Model):
    heading = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to='frontend_schoolsummery', default='thumbnail.jpg')
    youtube_link = models.TextField()
    description = models.TextField()
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'schoolsummery'

    def __str__(self):
        return self.heading

class About(models.Model):
    about_heading = models.CharField(max_length=70)
    about_description = models.CharField(max_length=355)
    about_background = models.ImageField(upload_to='frontend_schoolsummery', default='thumbnail.jpg')
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))
    # second part 
    class Meta:
        ordering = ['-id']
        db_table = 'about'

    def __str__(self):
        return self.about_heading

class ExtraCources(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField('Advertise Image, (310x160) size recommended',upload_to='frontend_cources', default='courcesdefault.jpg')
    price = models.IntegerField()
    faculty = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    description = models.TextField()
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'extracources'

    def __str__(self):
        return self.name

class Events(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField('Image (280x170) zise recommended',upload_to='frontend_events', default='eventdefault.jpg')
    heading = models.CharField(max_length=255)
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    city = models.CharField(max_length=100)
    description = models.TextField()
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'events'

    def __str__(self):
        return self.name

class RegisterNow(models.Model):
    heading = models.CharField('heading (max-value: 100 charators)',max_length=100)
    end_date = models.DateField('Ending Date of this offer')
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'registernow'

    def __str__(self):
        return self.heading

class RegisteredStudent(models.Model):
    register_for = models.ForeignKey(RegisterNow, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=21)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))
    
    class Meta:
        ordering = ['-id']
        db_table = 'registeredstudent'

    def __str__(self):
        return self.name
    
class Gallery(models.Model):
    heading = models.CharField('heading (max-value: 20 charators)',max_length=20)
    image = models.ImageField(upload_to='gallery')
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'gallery'

    def __str__(self):
        return self.heading
    
class NoticeBoard(models.Model):
    heading = models.CharField('heading (max-value: 20 charators)',max_length=20)
    date = models.DateField()
    description = models.TextField()
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'noticeboard'

    def __str__(self):
        return self.heading