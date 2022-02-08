from django.shortcuts import render, redirect
from student.models import Admission
from .forms import SearchChallan
from django.utils import timezone
from django.db.models import Q
from .models import Voucher
from payroll.models import Salary
from django import forms
from django.contrib import messages
from django.urls import reverse_lazy
from django import forms
from django.db.models import Sum, Count
from django.http import HttpResponse, JsonResponse
import datetime
import json
from academic.models import Section, Classes
from num2words import num2words
# Create your views here.
from django.contrib.auth.mixins import PermissionRequiredMixin
from home.decorators import allowed_users
from django.contrib.auth.decorators import login_required
from payroll.models import Teacher
from home.views import SchoolProfile
from django.contrib.auth.models import User
# Fee section

class FeeDefSerchForm(forms.Form):

    seacher_date = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'date seacher_date',
                'value': timezone.now().strftime('%Y-%m-%d')
            }
        )
    )


class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = '__all__'




def convert_month(month_val):
    if len(str(month_val))<2:
        return '0'+str(month_val)
    else:
        return month_val

def generate_voucher_number(number):
    """ NEED AN INTEGER generate_voucher_number(number objects) """
    sno = ''
    number = int(number)+1
    number = str(number)
    if len(number)<2:
        sno = '00000000'+number
    elif len(number)<3:
        sno = '0000000'+number
    elif len(number)<4:
        sno = '000000'+number
    elif len(number)<5:
        sno = '00000'+number
    elif len(number)<6:
        sno = '0000'+number
    elif len(number)<7:
        sno = '000'+number
    elif len(number)<8:
        sno = '00'+number
    elif len(number)<9:
        sno = '0'+number
    else:
        sno = number
    return sno



@login_required
# @allowed_users('add_voucher')
def fee_main(request):
    month = timezone.now().strftime("%m")
    current_month = timezone.now().strftime("%Y-%m-%d")
    year = timezone.now().strftime("%Y")

    if request.user.is_staff:
        module_holder = request.user.username
    else:
        this_holder = Teacher.objects.get(user_ptr_id=request.user.id)
        module_holder = this_holder.module_holder

    # GETTING MONTHLY FEE
    current_month_total_fee = Voucher.objects.filter(
        month=month,
        fee_month=current_month,
        year=year,
        module_holder=module_holder 
        ).aggregate(current_month_total_fee=Sum('monthly_tution_fee_paid'))

    # GETTING YEALY FEE
    current_year_total_fee = Voucher.objects.filter(
        year=year,
        module_holder=module_holder
        ).aggregate(current_year_total_fee=Sum('monthly_tution_fee_paid'))
    
    # GETTING MONTHLY SALARY TOTAL
    current_month_total_salary = Salary.objects.filter(
        Q(Salary_date__startswith=timezone.now().strftime('%Y-%m'),
        module_holder=module_holder)
        ).aggregate(monthly_salary=Sum('salary'))

    # GETTING yearly SALARY TOTAL
    current_year_total_salary = Salary.objects.filter(
        Q(Salary_date__startswith=timezone.now().strftime('%Y'),
        module_holder=module_holder)
        ).aggregate(yearly_salary=Sum('salary'))

    print(current_month_total_salary,'====================================')
    # # GETTING UNPAID VOUCHER MONTHLY
    # current_unpaid_Vouchers_monthly = Voucher.objects.filter(
    #     month = month,
    #     year = year,
    #     monthly_tution_fee_paid=0,
    #     module_holder=module_holder
    # ).count()

    # # GETTING UNPAID VOUCHER YEARLY
    # current_unpaid_Vouchers_yearly = Voucher.objects.filter(
    #     year = year,
    #     monthly_tution_fee_paid=0,
    #     module_holder=module_holder
    # ).count()

    data_chart= []
    for month in range(1, 13):
        paid =  Voucher.objects.filter(module_holder=module_holder, year=year, month=convert_month(month), monthly_tution_fee_paid__gt=1).aggregate(paid = Sum('monthly_tution_fee_paid'))
        unpaid = Voucher.objects.filter(module_holder=module_holder, year=year, month=convert_month(month), monthly_tution_fee_paid__lt=1).aggregate(unpaid = Sum('monthly_tution_fee') )
        
        data_chart.append({
            'paid': paid,
            'unpaid': unpaid,
            'date': year+'-'+str(convert_month(month))+'-'+'01'
        })
    final_chart=[]
    for data in data_chart:
        if data['paid']['paid'] is None:
            paid = 0
        else:
            paid = data['paid']['paid']

        if data['unpaid']['unpaid'] is None:
            unpaid = 0
        else:
            unpaid = data['unpaid']['unpaid']
        final_chart.append({
            'paid_amount': paid,
            'un_paid_amount': unpaid,
            'date': data['date'],
            
        })
        
    
    print(final_chart)
    ddddd = json.dumps(final_chart)
    context = {
        'data_chart': final_chart,
        'ddddd': ddddd,
        'current_year_total_salary':current_year_total_salary,
        'current_month_total_salary': current_month_total_salary,
        'current_month_total_fee': current_month_total_fee,
        'current_year_total_fee': current_year_total_fee,
        # 'current_unpaid_Vouchers_monthly': current_unpaid_Vouchers_monthly,
        # 'current_unpaid_Vouchers_yearly': current_unpaid_Vouchers_yearly,
        'current_month': timezone.now().strftime('%B, %Y'),
        'current_month_redirect': timezone.now().strftime('%Y-%m-%d'),
        'current_year': timezone.now().strftime('%Y'),
        'current_month_total_fee': current_month_total_fee
    }
    return render(request,'fee/main.html', context)

@login_required
@allowed_users('view_voucher')
def fee_received(request, date):
    if request.user.is_staff:
        module_holder = request.user.username
    else:
        this_holder = Teacher.objects.get(user_ptr_id=request.user.id)
        module_holder = this_holder.module_holder    
    if len(date)>4:
        searched_data_month = Voucher.objects.filter(module_holder=module_holder, month=date.split('-')[1], fee_month=date, year=date.split('-')[0], monthly_tution_fee_paid__gt=1)
    else:
        searched_data_month = Voucher.objects.filter(module_holder=module_holder, year=date, monthly_tution_fee_paid__gt=1)
    
    context = {
        'searched_data_month': searched_data_month
    }
    return render(request, 'fee/fee_received.html', context)


@login_required
# @allowed_users('view_voucher')    
def GenerateChallan(request):
    all_vouchers = [] 
    if request.user.is_staff:
        module_holder = request.user.username
    else:
        this_holder = Teacher.objects.get(user_ptr_id=request.user.id)
        module_holder = this_holder.module_holder
    if request.method=='POST':
        search_form = SearchChallan(module_holder, request.POST, initial={'year':timezone.now().strftime('%Y')})
        if search_form.is_valid():

            class_id = request.POST.get('classes')
            section_id = request.POST.get('admission_section')
            # issue_date = request.POST.get('issue_date'),
            # due_date = request.POST.get('due_date'),
            # fee_month = request.POST.get('fee_month'),
            year = request.POST.get('fee_month').split('-')[0],
            year = year[0]
            all_std = Admission.objects.filter(module_holder=module_holder, admission_class=class_id, admission_section=section_id)
            # print('===================\n', request.POST)
            for data in all_std:
                search_voucher_data = Voucher.objects.filter(
                    student_name=Admission.objects.get(pk=data.pk), 
                    father_name=data.father_name, 
                    month=request.POST.get('fee_month').split('-')[1],
                    year=year,
                    module_holder=module_holder
                )
                
                if search_voucher_data.exists():
                    search_voucher_data.update(issue_date=request.POST.get('issue_date'),due_date=request.POST.get('due_date'))
                    messages.success(request, 'Data has been updated & ready to print')
                else:
                    messages.success(request, 'Data has been Saved & ready to print')
                    if Voucher.objects.count()>0:
                        challan_number = Voucher.objects.values('id').latest('id')['id']
                    else:
                        challan_number ='0'
                    #COLCULATING FEE WITH ADMISSION DATE 
                    monthly_tution_fee_divided_in_days = 0
                    admission_date = str(data.admission_date).split('-')
                    admission_year = int(admission_date[0])
                    admission_month = int(admission_date[1])
                    admission_day = int(admission_date[2])
                    challan_year = int(request.POST.get('fee_month').split('-')[0])
                    challan_month = int(request.POST.get('fee_month').split('-')[1])

                    if(admission_year==challan_year and admission_month==challan_month):
                        monthly_tut_fee = data.monthly_tution_fee
                        per_day_fee = monthly_tut_fee/30
                        days_of_fee = 30-admission_day
                        monthly_tution_fee_divided_in_days = per_day_fee*days_of_fee
                    else:
                        monthly_tution_fee_divided_in_days = data.monthly_tution_fee
                    if(admission_year<=challan_year and admission_month<=challan_month):
                        save_voucher = Voucher( 
                        reg_number= data.admission_registration,
                        student_name=Admission.objects.get(pk=data.pk),
                        father_name=data.father_name,
                        issue_date=request.POST.get('issue_date'),
                        due_date=request.POST.get('due_date'),
                        fee_month=request.POST.get('fee_month'),
                        month= request.POST.get('fee_month').split('-')[1] ,
                        year=year,
                        challan_number=generate_voucher_number(challan_number),
                        monthly_tution_fee= monthly_tution_fee_divided_in_days,
                        section=data.admission_section,
                        class_name= data.admission_class,
                        module_holder = module_holder
                        ).save()                    
                    
                all_vouchers_single = Voucher.objects.filter(
                    student_name=Admission.objects.get(pk=data.pk), 
                    father_name=data.father_name, 
                    month=request.POST.get('fee_month').split('-')[1],
                    year=year,
                )
                
                all_vouchers.append({'voucher':all_vouchers_single})

    else:
        search_form = SearchChallan(module_holder ,initial={'year':timezone.now().strftime('%Y')})
          

    context = {
        'search_form': search_form,
        'all_student': all_vouchers,
        'current_month': timezone.now().strftime('%B, %Y'),
        'current_year': timezone.now().strftime('%Y')
    }
    return render(request, 'fee/generate_challan.html', context)


@login_required
# @allowed_users('view_voucher')
def generated_challan(request):
    if request.user.is_staff:
        module_holder = request.user.username
    else:
        this_holder = Teacher.objects.get(user_ptr_id=request.user.id)
        module_holder = this_holder.module_holder
    murge_data = []
    if request.method=='POST':
        
        print(request.POST)
        index=0
        for datas in request.POST.getlist('pk'):  
            data = {
                'reg_number': request.POST.getlist('reg_number')[int(datas)],
                'student_name':request.POST.getlist('name_of_student')[int(datas)],
                'father_name':request.POST.getlist('father_name')[int(datas)],
                'issue_date':request.POST.get('issue_date'),
                'due_date':request.POST.get('due_date'),
                'fee_month':request.POST.get('fee_month'),
                'year':request.POST.get('year'),
                'challan_number':request.POST.getlist('challan_number')[int(datas)],
                'monthly_tution_fee': request.POST.getlist('monthly_tution_fee')[int(datas)],
                'section':  request.POST.getlist('admission_section')[int(datas)],
                'class_name': request.POST.getlist('admission_class')[int(datas)],
                'monthly_tution_fee_in_word': num2words(request.POST.getlist('monthly_tution_fee')[int(datas)])
            }   
            for ps in range(0, 2):
                copy = ''
                if ps is 0:
                    copy="Parent's Copy"
                else:
                    copy="School Copy"

                murge_data.append({
                    'copy': copy,
                    'data': data
                })
            
            # if Voucher.objects.count()>0:
            #     challan_number = Voucher.objects.values('id').latest('id')['id']
            # else:
            #     challan_number ='0'

            # save_voucher = Voucher( 
            #         reg_number= request.POST.getlist('reg_number')[index],
            #         student_name=Admission.objects.get(name_of_student=request.POST.getlist('name_of_student')[index]),
            #         father_name=request.POST.getlist('father_name')[index],
            #         issue_date=request.POST.get('issue_date'),
            #         due_date=request.POST.get('due_date'),
            #         fee_month=request.POST.get('fee_month'),
            #         month= request.POST.get('fee_month').split('-')[1] ,
            #         year=request.POST.get('year'),
            #         challan_number=generate_voucher_number(challan_number),
            #         monthly_tution_fee= request.POST.getlist('monthly_tution_fee')[index],
            #         section= Section.objects.get(section_name=request.POST.getlist('admission_section')[index]) ,
            #         class_name= Classes.objects.get(class_name=request.POST.getlist('admission_class')[index]) ,
            #         module_holder = 'masood'
            # ).save()

            # voucher_form = VoucherForm(request.POST)
            # if voucher_form.is_valid():
            #     save_voucher.save()
            index = index+1 

    
    
    user = User.objects.get(username=module_holder)
    school_profile = SchoolProfile.objects.filter(username=user.pk).first()

    # print('==================user profile', school_profile.school_logo.url)
    context = {
        'school_profile': school_profile,
        'murge_data': murge_data,
        'current_month': timezone.now().strftime('%B, %Y'),
        'current_year': timezone.now().strftime('%Y')
    }
    return render(request, 'fee/generated_challan.html', context)
    

@login_required
@allowed_users('view_voucher')
def UnpaidChallan(request):
    if request.user.is_staff:
        module_holder = request.user.username
    else:
        this_holder = Teacher.objects.get(user_ptr_id=request.user.id)
        module_holder = this_holder.module_holder
    all_vouchers = []
    if request.method=='POST':
        search_form = SearchChallan(module_holder, request.POST, initial={'year':timezone.now().strftime('%Y')})
        if search_form.is_valid():
            # print(request.POST,'========form is valid')
            search_voucher_data = Voucher.objects.filter(
                    class_name=Classes.objects.get(pk=request.POST.get('classes')),
                    section = Section.objects.get(pk=request.POST.get('admission_section')),
                    # issue_date = request.POST.get('issue_date'),
                    # due_date = request.POST.get('due_date'),
                    # fee_month = request.POST.get('fee_month'),
                    month=request.POST.get('fee_month').split('-')[1],
                    year=request.POST.get('year'),
                    module_holder = module_holder
                )
            status = 0
            
            
            for data in search_voucher_data:
                if data.monthly_tution_fee_paid>0:
                    status = data.monthly_tution_fee_paid
                else:
                    status = 0
                all_vouchers.append({
                'pk':data.pk,
                'challan_number':data.challan_number,
                'reg_number':data.reg_number ,
                'monthly_tution_fee':data.monthly_tution_fee ,
                'status':status,
                'student_name':data.student_name ,
                'father_name':data.father_name,
                'section':data.section ,
                'class_name':data.class_name ,
                
                })
            if len(all_vouchers)>0:
                print("not empty")
            else:
                messages.warning(request," There is no any Challan Generated based on your searched data. Please Generate ")

    else:
        search_form = SearchChallan(module_holder, initial={'year':timezone.now().strftime('%Y')})
          

    context = {
        'search_form': search_form,
        'all_student': all_vouchers, 
        'current_month': timezone.now().strftime('%B, %Y'),
        'current_year': timezone.now().strftime('%Y')
    }
    return render(request, 'fee/unpaid_challan.html', context)


@login_required
@allowed_users('view_voucher')
def payChallan(request):
    if request.user.is_staff:
        module_holder = request.user.username
    else:
        this_holder = Teacher.objects.get(user_ptr_id=request.user.id)
        module_holder = this_holder.module_holder
    all_vouchers = []
    if request.method=='POST':
        search_form = SearchChallan(module_holder, request.POST, initial={'year':timezone.now().strftime('%Y')})
        if search_form.is_valid():
            # print(request.POST, 'this is valid=============')
            
            for pk_index in request.POST.getlist('pk'):
                pk = pk_index.split('-')[0]
                index = pk_index.split('-')[1]
                get_voucher_data = Voucher.objects.filter(pk=pk).update(
                    monthly_tution_fee_paid=request.POST.getlist('monthly_tution_fee')[int(index)]
                )
                

            search_voucher_data = Voucher.objects.filter(
                    class_name=request.POST.get('classes'),
                    section =request.POST.get('admission_section'),
                    # issue_date = request.POST.get('issue_date'),
                    # due_date = request.POST.get('due_date'),
                    month=request.POST.get('fee_month').split('-')[1],
                    year=request.POST.get('year'),
                    module_holder = module_holder
            )
            status = 0            
            
            for data in search_voucher_data:
                if data.monthly_tution_fee_paid>0:
                    status = data.monthly_tution_fee_paid
                else:
                    status = 0

                all_vouchers.append({
                'pk':data.pk,
                'challan_number':data.challan_number,
                'reg_number':data.reg_number ,
                'monthly_tution_fee':data.monthly_tution_fee ,
                'status':status,
                'student_name':data.student_name ,
                'father_name':data.father_name,
                'section':data.section ,
                'class_name':data.class_name
                })
            if len(all_vouchers)>0:
                print("not empty")
            else:
                messages.warning(request," There is no any Challan Generated based on your searched data. Please Generate Challan ")

    else:
        search_form = SearchChallan(module_holder, initial={'year':timezone.now().strftime('%Y')})
          

    context = {
        'search_form': search_form,
        'all_student': all_vouchers,
        'now': timezone.now().strftime('%m/%d/%Y')
    }
    return render(request, 'fee/unpaid_challan.html', context)


@login_required
@allowed_users('view_voucher')
def fee_defaulter(request):
    if request.user.is_staff:
        module_holder = request.user.username
    else:
        this_holder = Teacher.objects.get(user_ptr_id=request.user.id)
        module_holder = this_holder.module_holder
    all_vouchers = []
    date = timezone.now().strftime('%Y-%m-%d')
    if request.method=='GET':
        search_voucher_data = Voucher.objects.filter(
                   Q(monthly_tution_fee_paid__lt=1,
                    month=date.split('-')[1],
                    year=date.split('-')[0],
                    module_holder = module_holder)
        )
    if request.method=='POST':
        Feedefserchform = FeeDefSerchForm(request.POST)
        search_voucher_data = Voucher.objects.filter(
                   Q(monthly_tution_fee_paid__lt=1,
                    month=request.POST.get('seacher_date').split('-')[1],
                    year=request.POST.get('seacher_date').split('-')[0],
                    module_holder = module_holder)
        )
        if search_voucher_data:
            print(search_voucher_data, 'this is valid=============')
            index = 0
            for pk_id in request.POST.getlist('pk'):
                get_voucher_data = Voucher.objects.filter(pk=pk_id).update(
                    monthly_tution_fee_paid=request.POST.getlist('monthly_tution_fee')[index]
                )
                index = index+1
                messages.warning(request," There is no any Challan Generated based on your searched data. Please Generate ")
        else:
            messages.warning(request," There is no fee defaulter in this month ")
    else:
        Feedefserchform = FeeDefSerchForm()

    status = 0
        
    for data in search_voucher_data:
        if data.monthly_tution_fee_paid>0:
            status = data.monthly_tution_fee_paid
        else:
            status = 0

        all_vouchers.append({
                'pk':data.pk,
                'challan_number':data.challan_number,
                'reg_number':data.reg_number ,
                'monthly_tution_fee':data.monthly_tution_fee ,
                'status':status,
                'student_name':data.student_name ,
                'father_name':data.father_name,
                'section':data.section ,
                'class_name':data.class_name ,
            })

        if len(search_voucher_data)>0:
            print("not empty")
        else:
            messages.warning(request," There is no any Challan Generated based on your searched data. Please Generate ")  

  
           

    context = {
        'all_student': all_vouchers,
        'Feedefserchform': Feedefserchform,
        'current_month': timezone.now().strftime('%B, %Y'),
        'current_year': timezone.now().strftime('%Y')
    }
    return render(request,'fee/fee_defaulter.html', context)