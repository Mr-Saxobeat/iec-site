# Generated by Django 3.1.7 on 2021-02-24 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vismet', '0024_inmetstationdata_solarins'),
    ]

    operations = [
        migrations.AddField(
            model_name='pixel',
            name='resolution',
            field=models.FloatField(default=0.05),
        ),
    ]