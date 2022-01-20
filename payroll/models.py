from django.db import models
from django.contrib.auth.models import  User
from django.utils import timezone
from django.urls import reverse_lazy
# Create your models here.

gender = [
    ('Male', 'Male'), ('Female', 'Female')
]

payment_method = [
    ('Cash', 'Cash'),
     ('Cheque', 'Cheque')
]


class Schedual(models.Model):
    time_in = models.CharField(max_length=10)
    time_out = models.CharField(max_length=10)
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'schedual'

    def __str__(self):
        return self.time_in+' to '+self.time_out

    def get_absolute_url(self):
        return reverse_lazy('payroll:schedual_view')


class Position(models.Model):
    position_title = models.CharField(max_length=50)
    rate_per_hour = models.IntegerField()
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'position'

    def __str__(self):
        return self.position_title

    def get_absolute_url(self):
        return reverse_lazy('payroll:position_view')


class Teacher(User):
    designation = models.CharField('Role', max_length=70)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=70, choices=gender, default='Male')
    religion = models.CharField(max_length=70, default='not mentioned')
    Phone = models.CharField(max_length=20)
    address = models.TextField()
    date_of_join = models.DateField()
    status = models.IntegerField(default=1)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='position_with_teacher')
    time_schedual = models.ForeignKey(Schedual, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='teachers', default='noimage.png')
    twitter = models.CharField(max_length=255, default='https://twitter.com/intelexcel')
    linkedin = models.CharField(max_length=255, default='https://linkedin.com/intel3xcel')
    facebook = models.CharField(max_length=255, default='https://facebook.com/intelexcel')
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))
    
    class Meta:
        ordering = ['-id']
        db_table = 'teacher'

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse_lazy('payroll:teacher_view')

class Leave(models.Model):
    employee = models.ForeignKey(Teacher, on_delete=models.CASCADE, default=0)
    date = models.DateField('Current Date')
    type = models.CharField(choices=[('h', 'Holiday'), ('l', 'Leave')], default='l', max_length=8)
    from_date = models.DateField()
    to_date = models.DateField()
    is_paid = models.BooleanField(default=1)
    reasion = models.CharField(max_length=50)
    leave_message = models.TextField()
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'leave'

    def __str__(self):
        return str(self.employee)

    def get_absolute_url(self):
        return reverse_lazy('payroll:leave_view')

    
class Salary(models.Model):
    employee_name = models.ForeignKey(Teacher, related_name='teacher_salary', on_delete=models.CASCADE)
    Salary_date = models.DateField()
    Salary_release_date = models.DateField()
    salary = models.IntegerField()
    bonus = models.IntegerField()
    other = models.IntegerField(default=0)
    advance_detected = models.IntegerField(default=0)
    details = models.CharField(max_length=255, default='No Message')
    payment_method = models.CharField(max_length=8, default='Cash', choices=payment_method)
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        get_latest_by = 'pk'
        db_table = 'salary'

    def get_absolute_url(self):
        return reverse_lazy('payroll:fee_main')

class AdvanceSalary(models.Model):
    employee_name = models.ForeignKey(Teacher, related_name='advancesalary', on_delete=models.CASCADE)
    advance_amount = models.IntegerField()
    payment_date = models.DateField()
    monthly_detection = models.IntegerField(default=0)
    detail = models.TextField()
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        get_latest_by = 'pk'
        db_table = 'advancesalary'

    def get_absolute_url(self):
        return reverse_lazy('payroll:advancesalary_view')



class EmployeeAttendance(models.Model):
    employee_name = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.CharField(max_length=10)
    time_out = models.CharField(max_length=10)
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        get_latest_by = 'pk'
        db_table = 'employeeattendance'

    def get_absolute_url(self):
        return reverse_lazy('payroll:employee_attendance')