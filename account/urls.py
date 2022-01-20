from django.urls import path
from .views import (
    FeetypeView,
    FeetypeCreate,
    FeetypeUpdate,
    FeetypeDelete,
    InvoiceDetailView,
    InvoiceDetailCreate,
    InvoiceDetailUpdate,
    InvoiceDetailDelete,
    ExpenseView,
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseDelete,
    IncomeView,
    IncomeCreate,
    IncomeUpdate,
    IncomeDelete,
    get_income_with_ajax,
    get_expense_with_ajax
)

app_name = 'account'
urlpatterns = [
    path('feetype/view', FeetypeView.as_view(), name='feetype_view'),
    path('feetype/create', FeetypeCreate.as_view(), name='feetype_create'),
    path('feetype/<int:pk>/update', FeetypeUpdate.as_view(), name='feetype_update'),
    path('feetype/<int:pk>/view', FeetypeDelete.as_view(), name='feetype_delete'),
    path('invoice/view', InvoiceDetailView.as_view(), name='invoice_view'),
    path('invoice/create', InvoiceDetailCreate.as_view(), name='invoice_create'),
    path('invoice/<int:pk>/update', InvoiceDetailUpdate.as_view(), name='invoice_update'),
    path('invoice/<int:pk>/view', InvoiceDetailDelete.as_view(), name='invoice_delete'),
    path('expense/view', ExpenseView.as_view(), name='expense_view'),
    path('expense/create', ExpenseCreate.as_view(), name='expense_create'),
    path('expense/<int:pk>/update', ExpenseUpdate.as_view(), name='expense_update'),
    path('expense/<int:pk>/view', ExpenseDelete.as_view(), name='expense_delete'),
    path('income/view', IncomeView.as_view(), name='income_view'),
    path('income/create', IncomeCreate.as_view(), name='income_create'),
    path('income/<int:pk>/update', IncomeUpdate.as_view(), name='income_update'),
    path('income/<int:pk>/view', IncomeDelete.as_view(), name='income_delete'),
    path('get_income_with_ajax', get_income_with_ajax, name="get_income_with_ajax"),
    path('get_expense_with_ajax', get_expense_with_ajax, name="get_expense_with_ajax")
]