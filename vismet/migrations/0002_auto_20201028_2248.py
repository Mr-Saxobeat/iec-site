# Generated by Django 3.1.2 on 2020-10-29 01:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vismet', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='city',
            old_name='cod_ibge',
            new_name='ibge_code',
        ),
        migrations.RenameField(
            model_name='city',
            old_name='lei_criaca',
            new_name='lei_criacao',
        ),
        migrations.RenameField(
            model_name='city',
            old_name='macroestad',
            new_name='macroestado',
        ),
        migrations.RenameField(
            model_name='city',
            old_name='microestad',
            new_name='microestado',
        ),
        migrations.RenameField(
            model_name='city',
            old_name='nome',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='city',
            old_name='percen_are',
            new_name='percen_area',
        ),
    ]
