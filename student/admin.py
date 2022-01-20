from django.contrib import admin
from .models import Admission, Attendance, StudentMark, MarkDistribution
# Register your models here.
admin.site.register([Admission, Attendance, StudentMark, MarkDistribution])

