from django.shortcuts import render
from django.views.generic import  CreateView, UpdateView, DeleteView, TemplateView
from django.core.mail import send_mail
from .models import Email
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from home.decorators import allowed_users
from django.contrib.auth.decorators import login_required
# Create your views here.


class MessageEmailView(TemplateView):
    template_name = 'message/message_email.html'

class MessageVIew(TemplateView):
    template_name = 'message/message.html'

class EmailView(TemplateView):
    template_name = 'message/email.html'

    def get_context_data(self, **kwargs):
        context = super(EmailView, self).get_context_data(**kwargs)
        module_holder = self.request.user.username
        context['mail_list'] = Email.objects.filter(module_holder=module_holder)
        return context


# class ComposeView(TemplateView):
#     template_name = 'message/compose.html'


class SendMail(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = 'home:login'
    model = Email
    fields = [
            'mail_from',
            'mail_to',
            'mail_cc',
            'subject',
            'attachment',
            'message'
        ]
    template_name = 'message/compose.html'
    success_message = 'Email has been sent'
    context_object_name = 'mail_list'
    
    def form_valid(self, form):
        module_holder = self.request.user.username
        form.instance.module_holder = module_holder
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(SendMail, self).get_context_data(**kwargs)
        module_holder = self.request.user.username
        context['mail_list'] = Email.objects.filter(module_holder=module_holder)
        return context
    

    # send_mail(
    #     'hello from masood',
    #     'this is automated message replay',
    #     'masoodazhar60@yahoo.com',
    #     ['masoodazhar60@gmail.com'],
    #     fail_silently=False
    #     )
    
   