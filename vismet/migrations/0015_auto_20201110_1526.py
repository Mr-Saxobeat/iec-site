# Generated by Django 3.1.2 on 2020-11-10 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vismet', '0014_auto_20201110_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='subsourcedetail',
            name='url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='subsource',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='subsourcedetail',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
