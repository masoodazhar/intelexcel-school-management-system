# Generated by Django 2.2.10 on 2020-09-10 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('websitesetting', '0004_mainsetting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='image',
            field=models.ImageField(default='eventdefault.jpg', upload_to='frontend_events', verbose_name='Image (280x170) zise recommended'),
        ),
        migrations.AlterField(
            model_name='extracources',
            name='image',
            field=models.ImageField(default='courcesdefault.jpg', upload_to='frontend_cources', verbose_name='Advertise Image, (310x160) size recommended'),
        ),
        migrations.AlterField(
            model_name='slider',
            name='back_image',
            field=models.ImageField(default='defaultslider.jpg', upload_to='frontend_sliders', verbose_name='Slider Back Image (2014x456) size recommended'),
        ),
    ]