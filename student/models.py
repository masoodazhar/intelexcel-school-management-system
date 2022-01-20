from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from academic.models import Classes, Section, Subject
from django.db.models import Q
from django.contrib.postgres.fields import ArrayField

# from django.http import HttpRequest

# print(request.session['school_user_id'],'======================sada=as=ad=asd=dasd=sd=sd=d=d=ssd=asd=')

options = [
    ('1', 'Present'),
    ('2', 'Absent'),
    ('3', 'Leave'),
    ('4', 'Late-In'),
    ('4', 'Off By School'),
]

month_name = [
    ('1', 'Jan'),
    ('2', 'Feb'),
    ('3', 'Mar'),
    ('4', 'Apr'),
    ('5', 'May'),
    ('6', 'Jun'),
    ('7', 'Jul'),
    ('8', 'Aug'),
    ('9', 'Sep'),
    ('10', 'Act'),
    ('11', 'Nov'),
    ('12', 'Dec')
]

types = [
    ('exam', 'Exam'),
    ('attendance', 'Attendance'),
    ('class test', 'Class Test'),
    ('assignment', 'Assignment'),
   
]
exam_type = [
    ('midterm', 'midterm'),
    ('final', 'final'),
    ('classtest', 'class test'),
    ('assignment', 'assignment')

]
# Create your models here.
gender = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
yes_no = [('0', 'NO'), ('1', 'YES')]

def get_default_something():
    return {'id': ['no'], 'reject_list': []}

class Admission(models.Model):
    admission_date = models.DateField()
    admission_class = models.ForeignKey(Classes, on_delete=models.CASCADE)
    admission_section = models.ForeignKey(Section, on_delete=models.CASCADE)
    admission_registration = models.CharField(max_length=35)
    name_of_student = models.CharField(max_length=35)
    father_name = models.CharField(max_length=35)
    father_cnic = models.CharField(max_length=35)
    cast = models.CharField(max_length=35, default='no')
    father_profession = models.CharField(max_length=35)
    date_of_birth = models.DateField()
    contact = models.CharField(max_length=35)
    address = models.TextField()
    gender = models.CharField(max_length=10, default='Male', choices=gender)
    recieve_admissin_fee_with_admission = models.CharField(default='no',max_length=15, choices=yes_no)
    monthly_tution_fee = models.IntegerField(default=0)
    concession_fee = models.IntegerField(default=0)
    annual_fund = models.IntegerField(default=0)
    free_student = models.CharField(default='no',max_length=3, choices=yes_no)
    father_email_address = models.EmailField(max_length=100 ,blank=True)
    Student_email_address = models.EmailField(max_length=100 ,blank=True)
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))
    photo = models.ImageField(upload_to='students', default='noimage.png')
    status = models.IntegerField(default=1)
    password = models.CharField(max_length=255, default="student123")
    status_date = models.DateField(default=timezone.now().strftime('%Y-%m-%d'))
    
    class Meta:
        ordering = ['-id']
        db_table = 'admission'

    def __str__(self):
        return self.name_of_student

    def get_absolute_url(self):
        return reverse_lazy('student:admission_view')


# class TutionFee(models.Model):
#     student_id = models.ForeignKey(Admission, on_delete=models.CASCADE)
#     tution_fee_month = models.CharField(max_length=10, choices=month_name)
#     tution_fee = models.IntegerField()
#     admission_fee = models.IntegerField()
#     scient_fee = models.IntegerField()
#     game_fee = models.IntegerField()
#     fee_card = models.IntegerField()
#     library_fee = models.IntegerField()
#     identity_card = models.IntegerField()
#     registration_fee = models.IntegerField()
#     late_admission_fee = models.IntegerField()
#     computer_fee = models.IntegerField()
#     prospectus_fee = models.IntegerField()
#     security_fee = models.IntegerField()
#     receive_annual_fund_with_admission = models.CharField(max_length=15, choices=[
#         ('no', 'NO'), ('yes', 'YES')])
#     paid_annual_fund = models.IntegerField()  # display after select
#     total_amount_received = models.IntegerField()
#     send_sms = models.CharField(max_length=15, choices=[
#         ('no', 'NO'), ('yes', 'YES')])
#     sms_message = models.TextField()
#     module_holder = models.CharField(max_length=50)
#     inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))


class Attendance(models.Model):
    student_id = models.ForeignKey(Admission, on_delete=models.CASCADE)
    registration = models.CharField(max_length=35)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    subjects = models.CharField(max_length=50)
    date = models.DateField()
    attendance_selection = models.CharField(max_length=20, choices=options, default='Present')
    remarks = models.TextField(default='No', null=True)
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))
    current_month = models.CharField(max_length=20, default=str(timezone.now().strftime('%m/%Y')))

    class Meta:
        ordering = ['-id']
        db_table = 'attendance'
        
    def get_absolute_url(self):
        return reverse_lazy('student:attendance_mark')

    def __str__(self):
        return str(self.student_id)

    

class StudentMark(models.Model):
    student_name = models.ForeignKey(Admission, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Classes, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam = models.FloatField()
    attendance = models.FloatField()
    class_test = models.FloatField()
    assignment = models.FloatField() 
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))
    current_month = models.CharField(max_length=20, default=str(timezone.now().strftime('%Y-%m')))
    class Meta:    
        ordering = ['-id']
        db_table = 'studentmark'

    def get_absolute_url(self):
        return reverse_lazy('student:student_mark')   



class MarkDistribution(models.Model):
    class_name = models.ForeignKey(Classes, on_delete=models.CASCADE)
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam = models.IntegerField()
    attendance = models.IntegerField()
    class_test = models.IntegerField()
    assignment = models.IntegerField()
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'markdistribution'

    def get_absolute_url(self):
        return reverse_lazy('student:mark_distribution_create')

class Exams(models.Model):
    exams_name = models.CharField(max_length=100, unique=True)
    class_name = models.ForeignKey(Classes, on_delete=models.CASCADE)
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=20, choices=exam_type)
    marks = models.IntegerField()
    exam_detail_file = models.FileField('Exam Or Assignment Detail File',upload_to='exams', default='nofile.pdf', blank=True)
    open_date = models.DateField()
    due_date = models.DateField()
    remarks = models.TextField(blank=True)
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))
    current_month = models.CharField(max_length=20, default=str(timezone.now().strftime('%Y-%m')))

    def __str__(self):
        return self.exams_name

    class Meta:
        ordering = ['-id']
        db_table = 'exams'

    def get_absolute_url(self):
        return reverse_lazy('student:view_exams')

class ExamEmail(models.Model):
    exam = models.ForeignKey(Exams, on_delete=models.CASCADE)
    student = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    # mark_assigned = models.IntegerField(default=0)
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))
    current_month = models.CharField(max_length=20, default=str(timezone.now().strftime('%Y-%m')))

    class Meta:
        ordering = ['-id']
        db_table = 'examemail'  

    def get_absolute_url(self):
        return reverse_lazy('student:create_exams')

class CalculateResults(models.Model):
    student = models.ForeignKey(Admission, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Classes, on_delete=models.CASCADE)
    exam = models.ForeignKey(ExamEmail, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.CharField(default='undeclared', max_length=20)
    total_marks = models.IntegerField(default=0)
    exam_type = models.CharField(max_length=50)
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))
    current_month = models.CharField(max_length=20, default=str(timezone.now().strftime('%Y-%m')))
    
    class Meta:
        ordering = ['-id']
        db_table = 'calculateresults'  

    def get_absolute_url(self):
        return reverse_lazy('student:create_exams')


class StudentsMarks(models.Model):
    exam =  models.ForeignKey(Exams, on_delete=models.CASCADE)
    student =  models.ForeignKey(Admission, on_delete=models.CASCADE)
    marks = models.IntegerField()
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))
    current_month = models.CharField(max_length=20, default=str(timezone.now().strftime('%Y-%m')))

    class Meta:
        ordering = ['-id']
        db_table = 'studentsmarks'  

    def get_absolute_url(self):
        return reverse_lazy('student:create_exams')
    