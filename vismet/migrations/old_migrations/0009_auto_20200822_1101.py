# Generated by Django 3.0.8 on 2020-08-22 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vismet', '0008_auto_20200822_1017'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HeatPixel',
            new_name='Pixel',
        ),
        migrations.RenameModel(
            old_name='HeatPixelData',
            new_name='PixelData',
        ),
    ]
