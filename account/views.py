from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import FeeType, InvoiceDetail, InvoiceAmount, Expense, Income
from django.http import JsonResponse
from django.urls import reverse_lazy
from django import forms
from academic.models import Classes, Section
from payroll.models import Teacher
from student.models import Admission
from .forms import InvoiceAmountForm, InvoiceDetailForm, SearchExpenseIncome
from django.utils import timezone
from django.db.models import Q, Sum
from fee.models import Voucher
from payroll.models import Salary
from django.db.models.functions import Coalesce

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from home.decorators import allowed_users
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.
# account section

def convert_month(month_val):
    if len(str(month_val))<2:
        return '0'+str(month_val)
    else:
        return month_val

class FeetypeView(PermissionRequiredMixin, LoginRequiredMixin,ListView):
    model = Expense
    # fields = ['feetype_name','feetype_note']
    template_name = 'account/feetype.html'    
    login_url = 'home:login'
    context_object_name = 'feetypes'
    permission_required = 'academic.add_teacher'


class FeetypeCreate(CreateView):
    model = Expense
    fields = ['feetype_name','feetype_note']
    template_name = 'account/feetype_add.html'    
    context_object_name = 'feetypes'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.instance.module_holder = module_holder
        return super().form_valid(form)

class FeetypeUpdate(UpdateView):
    model = FeeType
    fields = ['feetype_name','feetype_note']
    template_name = 'account/feetype_add.html'    
    context_object_name = 'feetypes'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.instance.module_holder = module_holder
        return super().form_valid(form)


class FeetypeDelete(DeleteView):
    model = FeeType
    success_url = reverse_lazy('account:feetype_view')

# START InvoiceDetail CREATE InvoiceDetail UPDATE AND DELETE ETC. START
class InvoiceDetailView(ListView):
    model = InvoiceDetail
    # fields = ['feetype_name','feetype_note']
    template_name = 'account/invoice.html'    
    context_object_name = 'invoices'


class InvoiceDetailCreate(CreateView):
    model = InvoiceDetail
    fields = ['class_name', 'student_name', 'date', 'payment_status', 'payment_method']
    template_name = 'account/invoice_add.html'    
    context_object_name = 'invoices'

    def get_form(self, **kwargs):
        form = super(InvoiceDetailCreate, self).get_form(**kwargs)
        form.fields['date'].widget = forms.TextInput(attrs={'type': 'date'})
        return form

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.instance.module_holder = module_holder
        return super().form_valid(form)

    def get(model, request):

        context = {
            'amountform':InvoiceAmountForm(initial={'module_holder': 'masood'}),
            'form': InvoiceDetailForm(initial={'module_holder': 'masood'})
        }
        return render(request, 'account/invoice_add.html', context)


    def post(self, request):
        invoice_detail = InvoiceDetailForm(request.POST)

        
        if invoice_detail.is_valid():
            invoice_detail.save()

            last_invoiceDetail_id = InvoiceDetail.objects.latest('pk')



            index = 0
            for invoiceform in request.POST.getlist('fee_types'):
                invoice_form_check = InvoiceAmountForm(request.POST)
                invoice_amount = InvoiceAmount(
                    invoicedetail = last_invoiceDetail_id,
                    fee_type = FeeType.objects.get(pk=request.POST.getlist('fee_types')[index]),
                    amount = request.POST.getlist('amount')[index],
                    discount = request.POST.getlist('discount')[index],
                    subtotal = request.POST.getlist('subtotal')[index],
                    paid_amount = request.POST.getlist('paid_amount')[index],
                    module_holder = request.POST.get('module_holder')
                )
                # invoice_amount.save()
                if invoice_form_check.is_valid():
                    invoice_amount.save()
                    print('invice amount saved ', index)
                else:
                    print('error in invoice saved')
                index = index+1

            print("valid ===================================")
            invoice_detail_form =  InvoiceDetailForm(request.POST, initial={'module_holder': 'masood'}) 
            InvoiceAmount_form = InvoiceAmountForm(request.POST, initial={'module_holder': 'masood'})
        else:
            invoice_detail_form =  InvoiceDetailForm(request.POST, initial={'module_holder': 'masood'}) 
            InvoiceAmount_form = InvoiceAmountForm(request.POST, initial={'module_holder': 'masood'})
            print("valid ===================================")
        
        print(request.POST)
        context = {
            'amountform':InvoiceAmount_form,
            'form': invoice_detail_form
        }
        return render(request, 'account/invoice_add.html', context)
        # return redirect('account:invoice_view')
        
        
    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailCreate, self).get_context_data(**kwargs)
        context['amountform'] = InvoiceAmountForm()
        return context



class InvoiceDetailUpdate(UpdateView):
    model = InvoiceDetail
    fields = ['feetype_name','feetype_note']
    template_name = 'account/invoice_add.html'   

    def get_form(self, **kwargs):
        form = super(InvoiceDetailCreate, self).get_form(**kwargs)
        form.fields['date'].widget = forms.TextInput(attrs={'type': 'date'})
        return form
        
    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.instance.module_holder = module_holder
        form = super().form_invalid(form)


class InvoiceDetailDelete(DeleteView):
    model = InvoiceDetail
    success_url = reverse_lazy('account:invoice_view')




def get_expense_with_ajax(request):
    fee_data = []
    income_data = []
    year = request.GET.get('year')
    module_holder = request.user.username
    for month in range(1 , 13):
        fee = Salary.objects.filter(
                Salary_date__startswith = (year,'-',convert_month(month)),
                salary__gte=1,
                module_holder = module_holder
            ).aggregate(salaey_of_month=Coalesce(Sum('salary'), 0))
            
        fee_data.append(fee['salaey_of_month'])

    for month in range(1, 13):
        salary = Expense.objects.filter(
                date__startswith=str(year)+'-'+str(convert_month(month)),
                module_holder = module_holder

            ).aggregate(expense_amount=Coalesce(Sum('amount'),0))

        income_data.append(salary['expense_amount'])
    context = {
            'fee_data': fee_data,
            'income_data':income_data,
            'total_income': sum(income_data),
            'total_fee': sum(fee_data)
        }
    return JsonResponse(context)



# WORKING WITH AJAX 
def get_income_with_ajax(request):
        fee_data = []
        income_data = []
        module_holder = request.user.username
        year = request.GET.get('year')
        for month in range(1 , 13):
            fee = Voucher.objects.filter(
                month = convert_month(month),
                year = year,
                monthly_tution_fee_paid__gte=1,
                module_holder = module_holder
            ).aggregate(fee_of_month=Coalesce(Sum('monthly_tution_fee_paid'), 0))
            
            fee_data.append(fee['fee_of_month'])

        for month in range(1, 13):
            salary = Income.objects.filter(
                date__startswith=str(year)+'-'+str(convert_month(month)),
                module_holder = module_holder

            ).aggregate(income_amount=Coalesce(Sum('amount'),0))

            income_data.append(salary['income_amount'])
        context = {
            'fee_data': fee_data,
            'income_data':income_data,
            'total_income': sum(income_data),
            'total_fee': sum(fee_data)
        }
        return JsonResponse(context)
       



# START HERE FOR EXPENSE HERE==========================================================
class ExpenseView(PermissionRequiredMixin, LoginRequiredMixin ,CreateView):
    model = Expense
    fields = ['name','date','amount','file','note']
    template_name = 'fee/expense.html' 
    login_url = 'home:login'
    permission_required = 'account.view_expense'   
    # context_object_name = 'expenses'

    def get_context_data(self, **kwargs):
        context = super(ExpenseView, self).get_context_data(**kwargs)
        context['search_form'] = SearchExpenseIncome()
        current_month = timezone.now().strftime('%Y-%m')
        if self.request.method=='POST':
            current_month = self.request.POST.get('date')[:7]
            context['search_form'] = SearchExpenseIncome(self.request.POST)
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        context['expenses'] = Expense.objects.filter(Q(date__startswith=current_month, module_holder=module_holder))
        salary_data = []
        expense_data = []
        year = 2020
        for month in range(1 , 13):
            salaey = Salary.objects.filter(
                Salary_date__startswith = (year,'-',convert_month(month)),
                salary__gte=1,
                module_holder = module_holder
            ).aggregate(salary_of_month=Coalesce(Sum('salary'), 0))
            
            salary_data.append(salaey['salary_of_month'])

        for month in range(1, 13):
            salary = Expense.objects.filter(
                date__startswith=str(year)+'-'+str(convert_month(month)),
                module_holder = module_holder
            ).aggregate(expense_amount=Coalesce(Sum('amount'),0))
            
            expense_data.append(salary['expense_amount'])

        context['salary_data'] = salary_data
        context['total_salary'] = sum(salary_data)
        context['expense_data'] = expense_data
        context['total_expense'] = sum(expense_data)
        return context
    


class ExpenseCreate(PermissionRequiredMixin, SuccessMessageMixin, LoginRequiredMixin ,CreateView):
    model = Expense
    fields = ['name','date','amount','file','note']
    template_name = 'fee/expense_add.html'    
    context_object_name = 'expenses'
    permission_required = 'account.add_expense' 
    login_url = 'home:login'
    success_message = 'Expense has been saved!'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.instance.module_holder = module_holder
        return super().form_valid(form)
    
    def get_form(self, **kwargs):
        form = super(ExpenseCreate, self).get_form(**kwargs)
        form.fields['date'].widget = forms.TextInput(attrs={'class': 'date', 'value': timezone.now().strftime('%Y-%m-%d')})
        return form


class ExpenseUpdate(PermissionRequiredMixin,SuccessMessageMixin, LoginRequiredMixin ,UpdateView):
    model = Expense
    fields = ['name','date','amount','file','note']
    template_name = 'fee/expense_add.html'    
    context_object_name = 'expenses'
    login_url = 'home:login'
    permission_required = 'account.change_expense' 
    success_message = 'Expense has been updated!'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.instance.module_holder = module_holder
        return super().form_valid(form)

    def get_form(self, **kwargs):
        form = super(ExpenseUpdate, self).get_form(**kwargs)
        form.fields['date'].widget = forms.TextInput(attrs={'class': 'date', 'value': timezone.now().strftime('%Y-%m-%d')})
        return form


class ExpenseDelete(PermissionRequiredMixin, LoginRequiredMixin ,DeleteView):
    permission_required = 'account.delete_expense' 
    login_url = 'home:login'
    model = Expense
    success_url = reverse_lazy('account:expense_view')


def covert_month(val):
    val = str(val)
    if len(val)<2:
        return '0'+val
    else:
        return val


# START HERE FOR EXPENSE HERE==========================================================
class IncomeView(PermissionRequiredMixin, LoginRequiredMixin ,CreateView):
    model = Income
    login_url = 'home:login'
    fields = ['name','date','amount','file','note']
    template_name = 'fee/income.html'
    permission_required = 'account.view_income' 

    def get_context_data(self, **kwargs):
        context = super(IncomeView, self).get_context_data(**kwargs)
        context['search_form'] = SearchExpenseIncome()
        current_month = timezone.now().strftime('%Y-%m')
        if self.request.method=='POST':
            current_month = self.request.POST.get('date')[:7]
            context['search_form'] = SearchExpenseIncome(self.request.POST)
            
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder

        context['incomes'] = Income.objects.filter(Q(date__startswith=current_month, module_holder=module_holder))
        
        fee_data = []
        income_data = []
        year = 2020
        
        for month in range(1 , 13):
            fee = Voucher.objects.filter(
                month = convert_month(month),
                year = year,
                monthly_tution_fee_paid__gte=1,
                module_holder = module_holder
            ).aggregate(fee_of_month=Coalesce(Sum('monthly_tution_fee_paid'), 0))
            
            fee_data.append(fee['fee_of_month'])

        for month in range(1, 13):
            salary = Income.objects.filter(
                date__startswith=str(year)+'-'+str(convert_month(month)),
                module_holder = module_holder

            ).aggregate(income_amount=Coalesce(Sum('amount'),0))

            income_data.append(salary['income_amount'])
        
       

        context['fee_data'] = fee_data
        context['total_fee'] = sum(fee_data)
        context['income_data'] = income_data
        context['total_income'] = sum(income_data)
        
        return context


class IncomeCreate(PermissionRequiredMixin, SuccessMessageMixin, LoginRequiredMixin ,CreateView):
    model = Income
    fields = ['name','date','amount','file','note']
    template_name = 'fee/income_add.html'    
    context_object_name = 'incomes'
    permission_required = 'account.add_income' 
    login_url = 'home:login'
    success_message = 'Other income has been included'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.instance.module_holder = module_holder
        return super().form_valid(form)
    
    def get_form(self, **kwargs):
        form = super(IncomeCreate, self).get_form(**kwargs)
        form.fields['date'].widget = forms.TextInput(attrs={'class': 'date', 'value': timezone.now().strftime('%Y-%m-%d')})
        return form


class IncomeUpdate(PermissionRequiredMixin, SuccessMessageMixin, LoginRequiredMixin ,UpdateView):
    model = Income
    fields = ['name','date','amount','file','note']
    template_name = 'fee/income_add.html'    
    context_object_name = 'incomes'
    permission_required = 'account.change_income' 
    login_url = 'home:login'
    success_message = 'Other income has been updated'

    def form_valid(self, form):
        if self.request.user.is_staff:
            module_holder = self.request.user.username
        else:
            this_holder = Teacher.objects.get(user_ptr_id=self.request.user.id)
            module_holder = this_holder.module_holder
        form.instance.module_holder = module_holder
        return super().form_valid(form)

    def get_form(self, **kwargs):
        form = super(IncomeUpdate, self).get_form(**kwargs)
        form.fields['date'].widget = forms.TextInput(attrs={'class': 'date', 'value': timezone.now().strftime('%Y-%m-%d')})
        return form


class IncomeDelete(PermissionRequiredMixin, LoginRequiredMixin ,DeleteView):
    permission_required = 'account.delete_income'
    login_url = 'home:login' 
    model = Income
    success_url = reverse_lazy('account:income_view')