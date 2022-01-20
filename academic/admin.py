from django.contrib import admin

# Register your models here.

from .models import Section, Subject, Classes, Routine
admin.site.register([ Section, Subject, Classes, Routine])
