from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ElementCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ElementVariable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('sigla', models.CharField(max_length=10)),
                ('unit', models.CharField(max_length=10)),
                ('chartType', models.CharField(max_length=10)),
                ('chartColor', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='ElementSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('data_model', models.CharField(blank=True, max_length=200, null=True)),
                ('variables', models.ManyToManyField(to='vismet.ElementVariable')),
                ('startDate', models.DateField(blank=True, null=True)),
                ('finalDate', models.DateField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sources', to='vismet.elementcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stations', to='vismet.ElementSource')),
                ('omm_code', models.CharField(blank=True, max_length=100, null=True)),
                ('inmet_code', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('altitude', models.FloatField(blank=True, null=True)),
                ('startDate', models.DateField(blank=True, null=True, verbose_name='Data de início de operação')),
                ('finalDate', models.DateField(blank=True, null=True, verbose_name='Data de fim de operação')),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='XavierStationData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='xavier_data', to='vismet.Station')),
                ('evapo', models.FloatField(blank=True, null=True, verbose_name='Evapotranspiração')),
                ('relHum', models.FloatField(blank=True, null=True, verbose_name='Umidade Relativa')),
                ('solarIns', models.FloatField(blank=True, null=True, verbose_name='Radiação Solar')),
                ('maxTemp', models.FloatField(blank=True, null=True, verbose_name='Temperatura Máxima')),
                ('minTemp', models.FloatField(blank=True, null=True, verbose_name='Temperatura Mínima')),
                ('windSpeed', models.FloatField(blank=True, null=True, verbose_name='Velocidade do Vento')),
            ],
        ),
        migrations.CreateModel(
            name='INMETStationData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inmet_data', to='vismet.Station')),
                ('maxTemp', models.FloatField(blank=True, null=True, verbose_name='Temperatura Máxima')),
                ('minTemp', models.FloatField(blank=True, null=True, verbose_name='Temperatura Mínima')),
                ('relHum', models.FloatField(blank=True, null=True, verbose_name='Umidade Relativa')),
                ('precip', models.FloatField(blank=True, null=True, verbose_name='Precipitação')),
            ],
        ),
        migrations.CreateModel(
            name='ANAStationData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ana_data', to='vismet.Station')),
                ('value', models.FloatField(blank=True, null=True, verbose_name='Valor')),
            ],
        ),
        migrations.CreateModel(
            name='Pixel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100, null=True, blank=True)),
                ('state', models.CharField(max_length=100, null=True, blank=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('geom', models.PolygonField(null=True)),
            ],
        ),
    ]
