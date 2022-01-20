from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class SchoolProfile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_no = models.CharField(default=0, max_length=25)
    cnic = models.CharField(max_length=100, default='')
    school_name = models.CharField(max_length=100, default='')
    school_logo = models.ImageField(upload_to='schoo_logo', default='noimage.png')
    school_registration_no = models.CharField(max_length=50, default='')
    address = models.TextField(default='')
    email_address = models.CharField(max_length=100,default='info@intelexcel.com')
    school_timing_from = models.CharField(max_length=20, default='09:00')
    school_timing_to = models.CharField(max_length=20, default='17:00')
    module_holder = models.CharField(max_length=50, default='')
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))
    
    class Meta:
        ordering = ['-id']
        db_table = 'schoolprofile'
    
    def get_absolute_url(self):
        return reverse_lazy('home:main_page')


class Setting(models.Model):
    school_timing_from = models.CharField(max_length=20, default='09:00')
    school_timing_to = models.CharField(max_length=20, default='17:00')

    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'setting'
    
    def get_absolute_url(self, **kwargs):
        return reverse_lazy('home:main_page')

class CsvFile(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=150,unique=True)
    profile = models.TextField()
    def __str__(self):
        return self.name