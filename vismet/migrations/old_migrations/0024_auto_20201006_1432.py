# Generated by Django 3.1.1 on 2020-10-06 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vismet', '0023_auto_20201006_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weatherstation',
            name='altitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
