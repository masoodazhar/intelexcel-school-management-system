# Generated by Django 2.2.10 on 2020-09-22 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_auto_20200910_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admission',
            name='status_date',
            field=models.DateField(default='2020-09-22'),
        ),
    ]
