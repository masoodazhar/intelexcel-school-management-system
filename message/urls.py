from django.urls import path

from .views import (
    MessageEmailView,
    EmailView,
    SendMail,
    MessageVIew
)

app_name = 'message'
urlpatterns = [
    path('', MessageEmailView.as_view(), name='message_email'),
    path('email/view', EmailView.as_view(), name='email_view'),
     path('email/compose', SendMail.as_view(), name='send_mail'),
     path('message/view', MessageVIew.as_view(), name='message_view'),
]