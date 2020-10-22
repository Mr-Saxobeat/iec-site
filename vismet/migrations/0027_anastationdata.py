# Generated by Django 3.1.2 on 2020-10-19 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vismet', '0026_auto_20201016_1435'),
    ]

    operations = [
        migrations.CreateModel(
            name='ANAStationData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('value', models.FloatField(blank=True, null=True, verbose_name='Valor')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ana_data', to='vismet.station')),
            ],
        ),
    ]