from django.urls import path
from .views import (
    student_dashboard,
    profile_detail,
    attendance,
    results,
    exam_activity,
    account_book
)


urlpatterns = [
    path('', student_dashboard, name="student_dashboard"),
    path('profile_detail/', profile_detail, name="profile_detail"),
    path('attendance/', attendance, name="attendance"),
    path('results/', results, name="results"),
    path('exam_activity/', exam_activity, name="exam_activity"),
    path('account_book/', account_book, name="account_book"),
]