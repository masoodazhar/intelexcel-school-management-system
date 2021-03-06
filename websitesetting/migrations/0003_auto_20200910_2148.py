# Generated by Django 2.2.10 on 2020-09-10 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('websitesetting', '0002_slider_redirect_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='registernow',
            name='inserted_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='registernow',
            name='module_holder',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='registernow',
            name='end_date',
            field=models.DateField(verbose_name='Ending Date of this offer'),
        ),
    ]
