# Generated by Django 2.2.10 on 2020-09-22 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('websitesetting', '0008_auto_20200923_0055'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=20, verbose_name='heading (max-value: 20 charators)')),
                ('image', models.ImageField(upload_to='gallery')),
                ('module_holder', models.CharField(max_length=50)),
                ('inserted_date', models.DateField(auto_now=True)),
            ],
            options={
                'db_table': 'gallery',
                'ordering': ['-id'],
            },
        ),
    ]
