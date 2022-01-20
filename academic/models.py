from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from payroll.models import Teacher
from django.contrib.postgres.fields import ArrayField
# import jsonfield
# Create your models here.
data=dict({'data': 'No Day'})

def get_default_something():
    return {'accept_list': ['No Day'], 'reject_list': []}

gender = [
    ('Male', 'Male'), ('Female', 'Female')
]

school_year = []

for year in range(2010, int(timezone.now().strftime('%Y'))+5):
    school_year.append((str(year),year))

school_day = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
]

subject_type = [
    ('Optional', 'Optional'),
    ('Mandatory', 'Mandatory')
]

class Section(models.Model):
    section_name = models.CharField(max_length=25, unique=True)
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-section_name']
        db_table = 'section'

    def get_absolute_url(self):
        return reverse_lazy('student:create_section')

    def __str__(self):
        return self.section_name

class Room(models.Model):
    room_name = models.CharField(max_length=20, unique=True)
    room_number =models.IntegerField(default=0, unique=True)
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'room'
    
    def __str__(self):
        return self.room_name
    
    def get_absolute_url(self):
        return reverse_lazy('academic:room_view')

    
class Classes(models.Model):
    class_name = models.CharField(max_length=20)
    class_number =models.IntegerField(unique=True)
    fee = models.IntegerField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    discount  = models.IntegerField(default=0)
    note = models.TextField(default='No Detail')
    
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'classes'
    
    def __str__(self):
        return self.class_name+' - '+self.section.section_name
    
    def get_absolute_url(self):
        return reverse_lazy('academic:classes_view')



class Subject(models.Model):
    class_name = models.CharField(max_length=100)
    subject_name = models.CharField(max_length=20)
    subject_code =models.CharField(max_length=25, unique=True)
    # teacher_name = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject_type = models.CharField(max_length=25, choices=subject_type)
    pass_mark = models.IntegerField()
    final_mark = models.IntegerField()
    note = models.TextField(default='No Detail')
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'subject'
    
    def __str__(self):
        return self.subject_name
    
    def get_absolute_url(self):
        return reverse_lazy('academic:subject_view')


class Routine(models.Model):
    date_from = models.DateField(null=True)
    date_to = models.DateField(null=True)
    class_name = models.ForeignKey(Classes, on_delete=models.CASCADE)
    section_name =models.ForeignKey(Section, on_delete=models.CASCADE)
    subject_name =models.ForeignKey(Subject, on_delete=models.CASCADE)
    school_day = ArrayField(models.CharField(max_length=200), blank=True)
    teacher_name = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    start_time = models.CharField(max_length=20)
    end_time = models.CharField(max_length=20)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'routine'
    
    def __str__(self):
        return str(self.class_name)
    
    def get_absolute_url(self):
        return reverse_lazy('academic:routine_view')
    

