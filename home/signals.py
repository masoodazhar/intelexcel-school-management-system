from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import SchoolProfile
from django.contrib.auth.models import Group
from django.utils import timezone
from django.contrib.auth.models import update_last_login

# @receiver(post_save, sender=SchooProfile)
# def create_SchooProfile(sender, instance, created,  **kwargs):
#     if created:
#         print('==================signals===============')
#         print(instance)
#         SchooProfile.objects.create(username=instance)
#         instance.schooprofile.save()



# @receiver(post_save, sender=InvoiceDetail)
# def save_InvoiceAmount(sender, instance,  **kwargs):
#         instance.invoiceamount.save()

@receiver(post_save, sender=User)
def create_SchoolProfile(sender, instance, created,  **kwargs):
    if created:
        print('=============school profile', instance)
        SchoolProfile.objects.create(username=instance, module_holder=instance)
        school_group = Group.objects.get(name='school_user')
        school_group.user_set.add(instance)
        update_last_login(None, instance)

# @receiver(post_save, sender=SchooProfile)
# def save_SchooProfile(sender, instance,  **kwargs):
#     print('=======================instance', instance)
#     instance.schooprofile.save()
