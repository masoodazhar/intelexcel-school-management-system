from django.contrib import admin
from .models import Teacher, Salary, Leave, Schedual,  Position
# Register your models here.
admin.site.register([Teacher, Salary, Leave, Schedual,  Position])
