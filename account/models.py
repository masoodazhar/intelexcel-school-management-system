from django.db import models
from django.urls import reverse_lazy
from academic.models import Classes
from student.models import Admission
from django.utils import timezone
# Create your models here.

paymentstatus = [
    ('Not Paid', 'Not Paid'),
    ('Partially Paid', 'Partially Paid'),
    ('Fully Paid', 'Fully Paid'),
]
paymentMethod = [
    ('Cash', 'Cash'),
    ('Cheque', 'Cheque'),
    
]

        


class FeeType(models.Model):
    feetype_name = models.CharField(max_length=50)
    feetype_note =models.TextField()
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'feetype'

    def __str__(self):
        return self.feetype_name

    def get_absolute_url(self):
        return reverse_lazy('account:feetype_view')

    
class InvoiceDetail(models.Model):
    class_name = models.ForeignKey(Classes, on_delete=models.CASCADE)
    student_name = models.ForeignKey(Admission, on_delete=models.CASCADE)
    date = models.DateField()
    payment_status = models.CharField(max_length=25, choices=paymentstatus)
    payment_method = models.CharField(max_length=10, choices=paymentMethod)
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'invoicedetail'

    def __str__(self):
        return self.payment_status

    def get_absolute_url(self):
        return reverse_lazy('account:invoice_view')


class InvoiceAmount(models.Model):
    invoicedetail = models.ForeignKey(InvoiceDetail, on_delete=models.CASCADE)
    fee_type = models.ForeignKey(FeeType, on_delete=models.CASCADE)
    amount = models.FloatField()
    discount = models.FloatField()
    subtotal = models.FloatField()
    paid_amount = models.FloatField()
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering=['-id']
        db_table = 'invoiceamount'
        
    def __str__(self):
        return str(self.fee_type)+' Paid '+str(self.paid_amount)


class Expense(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField()
    amount = models.IntegerField()
    file = models.FileField(upload_to='files', default='not')
    note = models.TextField('Detail',default='No Detail')
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'expense'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('account:expense_view')


class Income(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField()
    amount = models.IntegerField()
    file = models.FileField(upload_to='files', default='not')
    note = models.TextField('Detail',default='No Detail')
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'income'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('account:income_view')