import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

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
                ('init', models.CharField(max_length=10)),
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
                ('geom', django.contrib.gis.db.models.fields.PolygonField(null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fid', models.BigIntegerField(blank=True, null=True)),
                ('nome', models.CharField(blank=True, max_length=50, null=True)),
                ('cod_ibge', models.FloatField(blank=True, null=True)),
                ('microestad', models.CharField(blank=True, max_length=50, null=True)),
                ('macroestad', models.CharField(blank=True, max_length=50, null=True)),
                ('fonte', models.CharField(blank=True, max_length=30, null=True)),
                ('data', models.CharField(blank=True, max_length=50, null=True)),
                ('area_km2', models.FloatField(blank=True, null=True)),
                ('perim_m', models.FloatField(blank=True, null=True)),
                ('percen_are', models.FloatField(blank=True, null=True)),
                ('origem', models.CharField(blank=True, max_length=100, null=True)),
                ('regional', models.CharField(blank=True, max_length=20, null=True)),
                ('estrutura', models.CharField(blank=True, max_length=30, null=True)),
                ('esc_local', models.CharField(blank=True, max_length=30, null=True)),
                ('lei_criaca', models.CharField(blank=True, max_length=250, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326)),
            ],
        ),
    ]
