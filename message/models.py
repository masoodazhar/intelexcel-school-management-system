from django.db import models
from django.utils import timezone
from django.urls import reverse_lazy
# Create your models here.


class Email(models.Model):
    subject = models.CharField('Subject:',max_length=255)
    mail_from = models.EmailField('from:')
    mail_cc = models.CharField('CC:',max_length=255, default='')
    mail_to = models.CharField("To:", max_length=255)
    message = models.TextField('Message')
    attachment = models.FileField(upload_to='messages/')
    module_holder = models.CharField(max_length=50)
    inserted_date = models.DateField(auto_now=timezone.now().strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['-id']
        db_table = 'email'

    def get_absolute_url(self):
        return reverse_lazy('message:email_view')
