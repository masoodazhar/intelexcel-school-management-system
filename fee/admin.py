from django.contrib import admin

# Register your models here.
from .models import  Voucher
from account.models import Expense, Income
admin.site.register([ Voucher, Income, Expense])
