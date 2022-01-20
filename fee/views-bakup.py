from django.shortcuts import render
from admission.models import Admission, Section, Classes
from .forms import SearchChallan
from django.utils import timezone
from django.db.models import Q
from .models import Voucher
from django import forms
from django.contrib import messages
# Create your views here.

class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = '__all__'


def generate_voucher_number(number):
    """ NEED AN INTEGER generate_voucher_number(number objects) """
    sno = ''
    number = int(number)+1
    number = str(number)
    if len(number)<2:
        sno = '00000'+number
    elif len(number)<3:
        sno = '0000'+number
    elif len(number)<4:
        sno = '000'+number
    elif len(number)<5:
        sno = '00'+number
    elif len(number)<6:
        sno = '0'+number
    else:
        sno = number
    return sno




def GenerateChallan(request):
    all_vouchers = [] 

    if request.method=='POST':
        search_form = SearchChallan(request.POST, initial={'year':timezone.now().strftime('%Y')})
        if search_form.is_valid():

            class_id = request.POST.get('classes')
            section_id = request.POST.get('admission_section')
            # issue_date = request.POST.get('issue_date'),
            # due_date = request.POST.get('due_date'),
            # fee_month = request.POST.get('fee_month'),
            year = request.POST.get('year'),

            all_std = Admission.objects.filter(admission_class=class_id, admission_section=section_id)
            # print('===================\n', request.POST)
            for data in all_std:
                search_voucher_data = Voucher.objects.filter(
                    student_name=Admission.objects.get(pk=data.pk), 
                    father_name=data.father_name, 
                    month=request.POST.get('fee_month').split('-')[1],
                    year=request.POST.get('year'),
                )
                
                if search_voucher_data.exists():
                    messages.success(request, 'Data has been updated & ready to print')
                else:
                    messages.success(request, 'Data has been Saved & ready to print')
                    if Voucher.objects.count()>0:
                        challan_number = Voucher.objects.values('id').latest('id')['id']
                    else:
                        challan_number ='0'
                        
                    save_voucher = Voucher( 
                        reg_number= data.admission_registration,
                        student_name=Admission.objects.get(pk=data.pk),
                        father_name=data.father_name,
                        issue_date=request.POST.get('issue_date'),
                        due_date=request.POST.get('due_date'),
                        fee_month=request.POST.get('fee_month'),
                        month= request.POST.get('fee_month').split('-')[1] ,
                        year=request.POST.get('year'),
                        challan_number=generate_voucher_number(challan_number),
                        monthly_tution_fee= data.monthly_tution_fee,
                        section= Section.objects.get(section_name=data.admission_section),
                        class_name= Classes.objects.get(class_name=data.admission_class),
                        module_holder = 'masood'
                        ).save()

                    
                
                all_vouchers_single = Voucher.objects.filter(
                    student_name=Admission.objects.get(pk=data.pk), 
                    father_name=data.father_name, 
                    month=request.POST.get('fee_month').split('-')[1],
                    year=request.POST.get('year'),
                )
                
                all_vouchers.append({'voucher':all_vouchers_single})


        print(all_vouchers)

    else:
        search_form = SearchChallan(initial={'year':timezone.now().strftime('%Y')})
          

    context = {
        'search_form': search_form,
        'all_student': all_vouchers,
        'now': timezone.now().strftime('%m/%d/%Y')
    }
    return render(request, 'fee/generate_challan.html', context)


def generated_challan(request):
    if request.method=='POST':
        murge_data = []
        print(request.POST)
        index=0
        for data in request.POST.getlist('name_of_student'):  
            data = {
                'reg_number': request.POST.getlist('reg_number')[index],
                'student_name':request.POST.getlist('name_of_student')[index],
                'father_name':request.POST.getlist('father_name')[index],
                'issue_date':request.POST.get('issue_date'),
                'due_date':request.POST.get('due_date'),
                'fee_month':request.POST.get('fee_month'),
                'year':request.POST.get('year'),
                'challan_number':request.POST.getlist('challan_number')[index],
                'monthly_tution_fee': request.POST.getlist('monthly_tution_fee')[index],
                'section':  request.POST.getlist('admission_section')[index],
                'class_name': request.POST.getlist('admission_class')[index],
            }   
            for ps in range(0, 2):
                print('===================================================\n')
                copy = ''
                if ps is 0:
                    copy="Parent's Copy"
                else:
                    copy="School Copy"

                murge_data.append({
                    'copy': copy,
                    'data': data
                })
            
            if Voucher.objects.count()>0:
                challan_number = Voucher.objects.values('id').latest('id')['id']
            else:
                challan_number ='0'

            save_voucher = Voucher( 
                    reg_number= request.POST.getlist('reg_number')[index],
                    student_name=Admission.objects.get(name_of_student=request.POST.getlist('name_of_student')[index]),
                    father_name=request.POST.getlist('father_name')[index],
                    issue_date=request.POST.get('issue_date'),
                    due_date=request.POST.get('due_date'),
                    fee_month=request.POST.get('fee_month'),
                    month= request.POST.get('fee_month').split('-')[1] ,
                    year=request.POST.get('year'),
                    challan_number=generate_voucher_number(challan_number),
                    monthly_tution_fee= request.POST.getlist('monthly_tution_fee')[index],
                    section= Section.objects.get(section_name=request.POST.getlist('admission_section')[index]) ,
                    class_name= Classes.objects.get(class_name=request.POST.getlist('admission_class')[index]) ,
                    module_holder = 'masood'
            ).save()

            # voucher_form = VoucherForm(request.POST)
            # if voucher_form.is_valid():
            #     save_voucher.save()
            index = index+1 





    context = {
        'murge_data': murge_data
    }
    return render(request, 'fee/generated_challan.html', context)
    





def UnpaidChallan(request):
    pass
    # all_student = []
    # if request.method=='POST':
    #     class_name = request.POST.get('classes')
    #     section = request.POST.get('admission_section')
    #     year = request.POST.get('year')
    #     issue_date = request.POST.get('issue_date')
    #     due_date = request.POST.get('due_date')
    #     search_form = SearchChallan(
    #         initial={
    #             'admission_section': section,
    #             'year': year,
    #             'classes': class_name,
    #             'issue_date': issue_date,
    #             'due_date': due_date
    #         }
    #     )

    #     all_student = Admission.objects.filter(Q(admission_class=class_name, admission_section=section))
    #     print('===============POST============')
    #     print(all_student)
    # else:
    #     print('==============ELSE=============')


    #     search_form = SearchChallan()
    # context = {
    #     'search_form': search_form,
    #     'all_student': all_student
    # }
    # return render(request, 'fee/unpaid_challan.html', context)