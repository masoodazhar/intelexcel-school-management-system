from django.db import models
from django.utils import timezone
from django.urls import reverse_lazy
from student.models import Admission
from academic.models import Section, Classes
# Create your models here.

payment_method = [
    ('Cash', 'Cash'),
     ('Cheque', 'Cheque')
]


        

class Voucher(models.Model):
    reg_number = models.CharField(max_length=25)
    student_name = models.ForeignKey(Admission, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=25)
    issue_date = models.DateField()
    due_date = models.DateField()
    fee_month = models.CharField(max_length=50)
    year = models.CharField(max_length=10)
    month = models.CharField(max_length=10)
    monthly_tution_fee = models.IntegerField()
    monthly_tution_fee_paid = models.IntegerField(default=0)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Classes, on_delete=models.CASCADE)
    challan_number = models.CharField(max_length=10)
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'voucher'

    def get_absolute_url(self):
        return reverse_lazy('fee:generated_challan')
    
