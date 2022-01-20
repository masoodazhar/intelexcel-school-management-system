# Generated by Django 2.2.10 on 2020-09-03 23:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CsvFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('address', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=150, unique=True)),
                ('profile', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_timing_from', models.CharField(default='09:00', max_length=20)),
                ('school_timing_to', models.CharField(default='17:00', max_length=20)),
                ('module_holder', models.CharField(max_length=50)),
                ('inserted_date', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['-id'],
                'db_table': 'setting',
            },
        ),
        migrations.CreateModel(
            name='SchoolProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_no', models.CharField(default=0, max_length=25)),
                ('cnic', models.CharField(default='', max_length=100)),
                ('school_name', models.CharField(default='', max_length=100)),
                ('school_logo', models.ImageField(default='noimage.png', upload_to='schoo_logo')),
                ('school_registration_no', models.CharField(default='', max_length=50)),
                ('address', models.TextField(default='')),
                ('school_timing_from', models.CharField(default='09:00', max_length=20)),
                ('school_timing_to', models.CharField(default='17:00', max_length=20)),
                ('module_holder', models.CharField(default='', max_length=50)),
                ('inserted_date', models.DateField(auto_now=True)),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
                'db_table': 'schoolprofile',
            },
        ),
    ]