# Generated by Django 2.2.10 on 2020-09-10 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('websitesetting', '0005_auto_20200911_0119'),
    ]

    operations = [
        migrations.AddField(
            model_name='registeredstudent',
            name='inserted_date',
            field=models.DateField(auto_now=True),
        ),
    ]
