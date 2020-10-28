# Generated by Django 3.1.1 on 2020-10-06 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vismet', '0021_weatherstation'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElementCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='weatherstation',
            name='geom',
        ),
        migrations.CreateModel(
            name='ElementSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('data_model', models.CharField(blank=True, max_length=200, null=True)),
                ('variables', models.CharField(max_length=500)),
                ('startDate', models.DateField(blank=True, null=True)),
                ('finalDate', models.DateField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sources', to='vismet.elementcategory')),
            ],
        ),
        migrations.AlterField(
            model_name='weatherstation',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stations', to='vismet.elementsource'),
        ),
    ]
