from django.shortcuts import render
from student.models import Admission, Attendance, Classes, MarkDistribution, StudentMark, CalculateResults, ExamEmail, Exams
from academic.models import Routine, Subject
from django.utils import timezone
from calendar import monthrange
import datetime
from student.views import attendance_converter, convert_month_into_string,calculate_student_fee_for_year
from .decorators import check_user_login
from django.db.models import Q, Sum
from fee.models import Voucher

start_year=2020
current_year = timezone.now().strftime('%Y')

all_months = ['01','02','03','04','05','06','07','08','09','10','11','12']

current_year = timezone.now().strftime('%Y')
# Create your views here.

@check_user_login
def student_dashboard(request):
    student_id = request.session['student_id']
    undeclared_exam_activity = 0
    try:
        admission = Admission.objects.get(pk=student_id)
        exams = Exams.objects.filter(class_name=admission.admission_class.pk)     
        
        
        undeclared_exam_activity = ExamEmail.objects.filter(student__contains=[str(student_id)], ).count()
        clear_exams = CalculateResults.objects.filter(~Q(marks = 'undeclared'),student=student_id ).count()
        # if calculated_marks and calculated_marks.marks is not 'undeclared':
        # print(clear_exams)
        undeclared_exam_activity = undeclared_exam_activity-clear_exams
            
                   
    except Exception as ex:
        print('error')

    # CALCULATING ATTENDANCE START
    percent_present = 0.0
    present_attendance = attendance(request, True)

    try:
        total_days = (366-present_attendance['total_off'])-present_attendance['total_holidays']
        percent_present =format((present_attendance['total_present']/total_days)*100, '.2f') 
        # print(percent_present)
    except Exception as ex:
        percent_present = 0
    # CALCULATING ATTENDANCE END
    
    # GETTING VOICHERS START
    total_unpaid_amount = 0
    unpain_vouchers = Voucher.objects.filter(student_name=student_id, monthly_tution_fee_paid__lt=1).count()
    unpaid_amount = Voucher.objects.filter(student_name=student_id, monthly_tution_fee_paid__lt=1).aggregate(total_unpaid_amount=Sum('monthly_tution_fee'))
    
    if unpaid_amount['total_unpaid_amount'] == None:
        total_unpaid_amount = 0
    else:
        total_unpaid_amount = unpaid_amount['total_unpaid_amount']
    

    context = {
        'undeclared_exam_activity': undeclared_exam_activity,
        'percent_present': percent_present,
        'unpain_vouchers': unpain_vouchers,
        'total_unpaid_amount': total_unpaid_amount
    }
    return render(request, 'student_dashboard/index.html', context)

@check_user_login
def profile_detail(request):
    student_id = request.session['student_id']
    student_data = {}
    days = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
    ]
    routines = []
    try:
        data = Admission.objects.get(pk=student_id)
        student_data = data
        for day in days:
            matched_routine = Routine.objects.filter(class_name=student_data.admission_class, school_day__contains=[day])
            routines.append({
                        'days':day,
                        'routine': matched_routine
            })
    except Exception as identifier:
        print(identifier)
    
    context = {
        'student_data': student_data,
        'days': days,
        'routines': routines
    }
    return render(request, 'student_dashboard/profile_detail.html', context)

@check_user_login
def attendance(request, incall=False):
    admission = request.session['student_id']
    student_attendance_detail_year = []
    monthly_detal = [] 
    total_holidays = 0
    total_leave = 0
    total_present = 0
    total_late = 0
    total_absent = 0  
    total_off = 0   
    for year in range(start_year, int(current_year)+1):
    # monthly_detal.clear()
        for month in all_months:
            # daily_detail.clear()
            for day in range(1, monthrange(year,int(month))[1]+1):
                if day < 10:
                    day = '0'+str(day)
                
                date = str(year)+'-'+str(month)+'-'+str(day)
                date = datetime.datetime.strptime(date,'%Y-%m-%d')
                daily = Attendance.objects.filter(student_id=admission, date=date)
                daily_inner = []
                if daily.exists():
                    for detail in daily:
                        if attendance_converter(detail.attendance_selection, date) == 'P':
                            total_present +=1
                        elif attendance_converter(detail.attendance_selection, date) == 'A':
                            total_absent +=1
                        elif attendance_converter(detail.attendance_selection, date) == 'O':
                            total_off +=1
                        elif attendance_converter(detail.attendance_selection, date) == 'H':
                            total_holidays +=1
                        elif attendance_converter(detail.attendance_selection, date) == 'L':
                            total_leave +=1
                        elif attendance_converter(detail.attendance_selection, date) == 'L-I':
                            total_late +=1
                        
                        # print('------------------------------')
                        # print(day)

                        daily_inner.append({
                            'day': day,
                            'month': convert_month_into_string(month),
                            'attendance': attendance_converter(detail.attendance_selection, date),
                            'remark': detail.remarks,
                            'att_date': detail.date
                        })
                else:
                    if attendance_converter('', date) == 'P':
                        total_present +=1
                    elif attendance_converter('', date) == 'A':
                        total_absent +=1
                    elif attendance_converter('', date) == 'O':
                        total_off +=1
                    elif attendance_converter('', date) == 'H':
                        total_holidays +=1
                    elif attendance_converter('', date) == 'L':
                        total_leave +=1
                    elif attendance_converter('', date) == 'L-I':
                        total_late +=1
                        
                    # print('------------------------------')
                    # print(day)
                    daily_inner.append({
                            'day': day,
                            'month': convert_month_into_string(month),
                            'attendance': attendance_converter('', date),
                            'remark': 'N/A',
                            'att_date': 'N/A'
                    })
                # daily_detail.append(daily_inner)
                monthly_detal.append(
                    {'daily': daily_inner}
                )
        student_attendance_detail_year.append({
            'year': year,
            'month': monthly_detal
        })
    context = {
        'student_attendance_detail_year': student_attendance_detail_year,
        'total_present': total_present,
        'total_absent': total_absent,
        'total_off': total_off,
        'total_holidays': total_holidays,
        'total_leave': total_leave,
        'total_late': total_late,
    }

    calculate_attendance = {
        'total_present': total_present,
        'total_off': total_off,
        'total_holidays': total_holidays
    }
    if incall:
        return calculate_attendance
    return render(request, 'student_dashboard/attendance.html', context)

@check_user_login
def results(request):
    student_id = request.session['student_id']
    admission = Admission.objects.get(pk=student_id)
    collect_std_marks_subs = []
    student_object = Admission.objects.filter(pk=student_id).first()
    class_of_student = Classes.objects.filter(class_name=student_object.admission_class.class_name).first()
    subjects = Subject.objects.filter(class_name__contains=class_of_student.pk)            
    get_calculated_marks = []
    for mos in subjects:
        out_of_marks = MarkDistribution.objects.filter(subject_name=mos.pk).first()
        in_of_marks = StudentMark.objects.filter(class_name=class_of_student.pk, subject=mos.pk, student_name=student_id).first()
        # marks_of_student = StudentMark.objects.filter(student_name=student_id)
        exam = 0
        attendance = 0
        assignment = 0
        class_test = 0

        calculated_marks_object = CalculateResults.objects.filter(student=admission, subject=mos.pk)
        for calc in calculated_marks_object:
            get_calculated_marks.append({
                'exam_type': calc.exam_type,
                'total_marks': calc.total_marks,
                'assigned_marks': calc.marks,
                'subject': calc.subject

            })
        if out_of_marks:
            in_of_marks = StudentMark.objects.filter(class_name=class_of_student.pk, subject=mos.pk, student_name=student_id).first()

            if in_of_marks:
                exam = in_of_marks.exam
                attendance = in_of_marks.attendance
                assignment = in_of_marks.assignment
                class_test = in_of_marks.class_test

            collect_std_marks_subs.append({
            'subject_name': mos.subject_name,
            'examout': out_of_marks.exam,
            'attendanceout': out_of_marks.attendance,
            'assignmentout': out_of_marks.assignment,
            'classtestout': out_of_marks.class_test,
            'examin': exam,
            'attendancin': attendance,
            'assignmentin': assignment,
            'classtestin': class_test


        })
        else:
            collect_std_marks_subs.append({
            'subject_name': mos.subject_name,
            'examout': 0,
            'attendanceout': 0,
            'assignmentout': 0,
            'classtestout': 0,
            'examin': exam,
            'attendancin': attendance,
            'assignmentin': assignment,
            'classtestin': class_test


        })
    # print(collect_std_marks_subs)
    # print('mamamamamam',subjects)

    # START WORKING WITH STUDENT PAYMENT SYSTEM
    

    context = {
        'collect_std_marks_subs': collect_std_marks_subs,
        'get_calculated_marks': get_calculated_marks
    }
    return render(request, 'student_dashboard/result.html', context)

@check_user_login
def exam_activity(request):
    student_id = request.session['student_id']
    admission = ''
    exam_lists = []
    try:
        admission = Admission.objects.get(pk=student_id)
        exams = Exams.objects.filter(class_name=admission.admission_class.pk)
        marks_status = 'Undeclared'
        for exam in exams:
            exam_emailed_to_student = ExamEmail.objects.filter(exam=exam, student__contains=[str(student_id)], ).first()
            if exam_emailed_to_student:
                calculated_marks = CalculateResults.objects.filter(exam=exam_emailed_to_student.pk, student=student_id, exam_type=exam.exam_type).first()
                if calculated_marks:
                    marks_status = calculated_marks.marks
                else:
                    marks_status = 'Undeclared'
                exam_lists.append({
                    'exam_name': exam.exams_name,
                    'exam_type': exam.exam_type,
                    'marks': exam.marks,
                    'exam_detail_file': exam.exam_detail_file,
                    'open_date': exam.open_date,
                    'due_date': exam.due_date,
                    'remarks': exam.remarks,
                    'subject_name': exam.subject_name,
                    'marks_status': marks_status
                })
                
        # status = 'not-sent'
        # exists_student = ExamEmail.objects.filter(student__contains=[str(student_id)])
        # if exists_student:
            
           
    except Exception as identifier:
        print(identifier)
    
    context = {
        'exam_lists': exam_lists
    }
    return render(request, 'student_dashboard/exam_activity.html', context)

@check_user_login
def account_book(request):

    if request.method =='POST':
        year = request.POST.get('year')
    else:
        year = timezone.now().strftime('%Y')
    student_id = request.session['student_id']
    admission = Admission.objects.get(pk=student_id)
    context = {
        'calculate_student_fee_for_year': calculate_student_fee_for_year(request,student_id, admission,year ),
        'range': range(2015,2030)
    }
    return render(request, 'student_dashboard/account_book.html',context)