# Generated by Django 3.0.8 on 2020-08-22 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vismet', '0007_auto_20200811_1447'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='XavierWeatherStation',
            new_name='XavierStation',
        ),
        migrations.RenameModel(
            old_name='StationData',
            new_name='XavierStationData',
        ),
    ]
