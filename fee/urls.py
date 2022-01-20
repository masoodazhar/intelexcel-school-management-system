from django.urls import path
from .views import (
        GenerateChallan,
        UnpaidChallan,
        generated_challan,
        payChallan,
        fee_defaulter,
        fee_main,
        fee_received
    )


app_name = 'fee'
urlpatterns = [
    path('', fee_main, name="fee_main"),
    path('generatechallan', GenerateChallan, name='generate_challan'),
    path('generatedChallan', generated_challan, name='generated_challan'),
    path('unpaidChallan/', UnpaidChallan, name='unpaid_challan'),
    path('payChallan', payChallan, name='pay_challan'),
    path('FR/<str:date>/fee_received', fee_received, name='fee_received'),  
    path('feedefaulter', fee_defaulter, name='fee_defaulter'),
]