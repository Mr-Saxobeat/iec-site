# Generated by Django 3.1.2 on 2020-10-29 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vismet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='elementsource',
            name='data_model',
        ),
        migrations.AddField(
            model_name='elementsource',
            name='data_model',
            field=models.ManyToManyField(to='vismet.DataModel'),
        ),
    ]