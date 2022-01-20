from django.urls import path
from .views import (
        TeacherCreate,
        TeacherView, 
        TeacherUpdate, 
        TeacherDelete,
        manage_salary,
        salary_monthly_detail,
        salary_detail_one,
        SchedualView,
        SchedualCreate,
        SchedualUpdate,
        SchedualDelete,
        PositionView,
        PositionCreate,
        PositionUpdate,
        PositionDelete,
        LeaveView,
        LeaveCreate,
        LeaveUpdate,
        LeaveDelete,
        employee_attendance,
        EmployeeAttednaceCreate,
        EmployeeAttednaceUpdate,
        employee_induigual,
        AdvanceSalaryView,
        AdvanceSalaryCreate,
        AdvanceSalaryUpdate,
        AdvanceSalaryDelete

    )


app_name = 'payroll'
urlpatterns = [
    path('',manage_salary , name="main_payroll"),

    path('advancesalary/view', AdvanceSalaryView.as_view(), name='advancesalary_view'),
    path('advancesalary/create', AdvanceSalaryCreate.as_view(), name='advancesalary_create'),
    path('advancesalary/<int:pk>/update', AdvanceSalaryUpdate.as_view(), name='advancesalary_update'),
    path('advancesalary/<int:pk>/delete', AdvanceSalaryDelete.as_view(), name='advancesalary_delete'),

    path('attendance/view', employee_attendance, name="employee_attendance"),
    path('attendance/<int:pk>/view', employee_induigual, name="employee_induigual"),
    path('attendance/add', EmployeeAttednaceCreate.as_view(), name="employee_attendance_add"),
    path('attendance/<int:pk>/edit', EmployeeAttednaceUpdate.as_view(), name="employee_attendance_update"),

    path('schedual/view', SchedualView.as_view(), name='schedual_view'),
    path('schedual/create', SchedualCreate.as_view(), name='schedual_create'),
    path('schedual/<int:pk>/update', SchedualUpdate.as_view(), name='schedual_update'),
    path('schedual/<int:pk>/delete', SchedualDelete.as_view(), name='schedual_delete'),

    path('position/view', PositionView.as_view(), name='position_view'),
    path('position/create', PositionCreate.as_view(), name='position_create'),
    path('position/<int:pk>/update', PositionUpdate.as_view(), name='position_update'),
    path('position/<int:pk>/delete', PositionDelete.as_view(), name='position_delete'),

    path('leave/view', LeaveView.as_view(), name='leave_view'),
    path('leave/create', LeaveCreate.as_view(), name='leave_create'),
    path('leave/<int:pk>/update', LeaveUpdate.as_view(), name='leave_update'),
    path('leave/<int:pk>/delete', LeaveDelete.as_view(), name='leave_delete'),

    path('teacher/view', TeacherView.as_view(), name='teacher_view'),
    path('teacher/create', TeacherCreate.as_view(), name='teacher_create'),
    path('teacher/<int:pk>/update', TeacherUpdate.as_view(), name='teacher_update'),
    path('teacher/<int:pk>/delete', TeacherDelete.as_view(), name='teacher_delete'),
    path('salary/', manage_salary, name='salary'),
    path('salary/<str:date>/monthly_detail',salary_monthly_detail, name='salary_monthly_detail' ),    
    path('salary/<int:pk>/<int:teacher_name_id>/monthly_detail_self',salary_detail_one, name='salary_detail_one' ),
  
]