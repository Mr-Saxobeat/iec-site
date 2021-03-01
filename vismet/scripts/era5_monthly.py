import datetime
import math
import os

import requests
import xarray as xr

from vismet.models import DataModel, Pixel, PixelData

def addMonth(date):
    if date.month == 12:
        return datetime.datetime(date.year + 1, 1, 1)
    else:
        return datetime.datetime(date.year, date.month + 1, date.day)

def run(path = '/home/weiglas/Documents/iec/dados/reanalise/era5/monthly/descompressed',
         date_str='1979-01-01',
         finalDate_str='2021-01-01',
         url='https://iec.ufes.br/plataforma/api/pixeldata/'):

    # Strings padrões do início e final de cada arquivo do ERA5
    file_init = '1month_mean_Global_ea_'
    file_final = '_v02.grib'

    # Data usada para montar o nome do arquivo e para preencher
    # o valor 'date' do model PixelData
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d')

    # Data usada para parar o programa
    finalDate = datetime.datetime.strptime(finalDate_str, '%Y-%m-%d')

    # Lista de todos arquivos no diretório (acho que iso não será usado)
    dir_files = os.listdir(path)

    # Caminho do arquivo de log, que vai registrar as falhas
    log_file_dir = os.path.join(os.getcwd(), 'pixel025_log.txt')
    log_file = open(log_file_dir, 'w')
    log_file.write('Coordenadas não encontradas')

    latitudes = []
    longitudes = []

    lat_dict = {}
    lon_dict = {}

    pixels = Pixel.objects.filter(resolution=0.25)
    data_model, created = DataModel.objects.get_or_create(name='era5')

    while(date.date() <= finalDate.date()):
        strDate = '_' + date.strftime('%Y%m')

        ds_2t = xr.open_dataset(os.path.join(path, file_init + '2t' + strDate + file_final), engine='cfgrib')
        # ds_ci = xr.open_dataset(os.path.join(path, file_init + 'ci' + strDate + file_final), engine='cfgrib')
        # ds_swvl1 = xr.open_dataset(os.path.join(path, file_init + 'swvl1' + strDate + file_final), engine='cfgrib')
        ds_r2 = xr.open_dataset(os.path.join(path, file_init + 'r2' + strDate + file_final), engine='cfgrib')
        ds_tp = xr.open_dataset(os.path.join(path, file_init + 'tp' + strDate + file_final), engine='cfgrib')

        # Preenche as listas de latitudes e longitudes
        # apenas na primeira vez, pois todos os arquivos
        # têm os mesmos valores.
        if len(latitudes) == 0:
            latitudes = ds_2t['latitude'].data.tolist()
            # Converte a longitude '0 ~ 360' para '-180 ~ +180'
            longitudes = ((ds_2t['longitude'] + 180) % 360 - 180).data.tolist()

        xr_2t = ds_2t['t2m']
        # xr_ci = ds_ci['siconc']
        # xr_swvl1 = ds_swvl1['swvl1']
        xr_r2 = ds_r2['r']
        xr_tp = ds_tp['tp']

        ds_2t.close()
        # ds_ci.close()
        # ds_swvl1.close()
        ds_r2.close()
        ds_tp.close()

        for p in pixels:

            # Blocos try para registrar o index da latitude
            # e longitude no dataset.
            try:
                i_lat = lat_dict[str(p.latitude)]
                i_lon = lon_dict[str(p.longitude)]
            except KeyError:
                try:
                    lat_dict[str(p.latitude)] = latitudes.index(p.latitude)
                    lon_dict[str(p.longitude)] = longitudes.index(p.longitude)

                    i_lat = lat_dict[str(p.latitude)]
                    i_lon = lon_dict[str(p.longitude)]
                except ValueError:
                    log_file.write(p.latitude + ', ' + p.longitude)
                    continue

            val_2t = xr_2t[i_lat, i_lon].data.tolist()
            # val_ci = xr_ci[i_lat, i_lon].data.tolist()
            # val_swvl1 = xr_swvl1[i_lat, i_lon].data.tolist()
            val_r2 = xr_r2[i_lat, i_lon].data.tolist()
            val_tp = xr_tp[i_lat, i_lon].data.tolist()

            val_2t = None if math.isnan(val_2t) else val_2t
            # val_ci = None if math.isnan(val_ci) else val_ci
            # val_swvl1 = None if math.isnan(val_swvl1) else val_swvl1
            val_r2 = None if math.isnan(val_r2) else val_r2
            val_tp = None if math.isnan(val_tp) else val_tp

            data = {
                'date': date.strftime('%Y-%m-%d'),
                'latitude': p.latitude,
                'longitude': p.longitude,
                'resolution': 0.25,
                'data_model_name': 'era5',
                'tp2m': val_2t,
                'relHum': val_r2,
                'precip': val_tp,
                # 'maxTemp': val_ci,
                # 'minTemp': val_swvl1,
            }

            response = requests.post(url, data=data, verify=False)

            if response.status_code == 200:
                print(str(response.status_code) + ': ' + str(p.latitude) + ', ' + str(p.longitude) + ' - ' + date.strftime('%m/%Y'))
            else:
                print(response.content)
                log_file.write(p.latitude + ', ' + p.longitude + ' -- ' + )
        
        date = addMonth(date)
    
    print('Data final alcançada. Finalizar.')
    log_file.close()









