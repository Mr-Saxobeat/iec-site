import os
import pandas
import requests
import datetime
import json
import math 

import xarray as xr

from vismet.models import Pixel, DataModel

# from vismet.scripts import era5_daily
# era5_daily.run(url='http://127.0.0.1:8000/plataforma/api/pixeldatalist/', finalDate_str='1981-01-01')
def run(path = '/home/weiglas/Documents/iec/dados/reanalise/era5/daily/',
        date_str='1981-01-01',
        finalDate_str='2021-01-01',
        url='https://iec.ufes.br/plataforma/api/pixeldatalist/'):

        # Data usada para início de gravaçãoes de dados
        curDate = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        # Data usada para parar o programa
        finalDate = datetime.datetime.strptime(finalDate_str, '%Y-%m-%d')

        # Caminho do arquivo de log, que vai registrar as falhas
        log_file_dir = os.path.join(os.getcwd(), 'era5_daily_log.txt')
        log_file = open(log_file_dir, 'w')

        pixels = Pixel.objects.filter(resolution=0.1)
        data_model, created = DataModel.objects.get_or_create(name='era5')
        
        while(curDate.date() <= finalDate.date()):
            latitudes = []
            longitudes = []
            lat_dict = {}
            lon_dict = {}
            data_list = []

            # dd = pandas.to_datetime(ds['time'][0].data.tolist()).date()

            try:
                ds = xr.open_dataset(os.path.join(path, curDate.date().strftime('%Y') + '.grib'), engine='cfgrib')
            except FileNotFoundError:
                print('Arquivo não encontrado  ' + path + curDate.date().strftime('%Y') + '.grib')
                log_file.write('Arquivo não encontrado   ' + path + curDate.date().strftime('%Y') + '.grib')
                continue

            u10 = ds['u10'].data.tolist() # 10m u-component of wind
            v10 = ds['v10'].data.tolist() # 10m v-component of wind
            t2m = ds['t2m'].data.tolist() # 2m temperature
            # slhf = ds['slhf'].data.tolist() # Surface latent heat flux
            # sshf = ds['sshf'].data.tolist() # Surface sensible heat flux
            # e = ds['e'].data.tolist() # Total evaporation
            tp = ds['tp'].data.tolist() # Total precipitation
            time = ds['time'].data.tolist()

            ds.close()

            # Preenche as listas de latitudes e longitudes
            # apenas na primeira vez, pois todos os arquivos
            # têm os mesmos valores.
            if len(latitudes) == 0:
                latitudes = ds['latitude'].data.tolist()
                longitudes = ds['longitude'].data.tolist()

            for p in pixels:
                data_list = []

                # Blocos try para registrar o index da latitude
                # e longitude no dataset.
                try:
                    # Procura o index no dict
                    i_lat = lat_dict[str(p.latitude)]
                    i_lon = lon_dict[str(p.longitude)]
                except KeyError:
                    try:
                        # Se não tiver, o registra no dict
                        lat_dict[str(p.latitude)] = latitudes.index(p.latitude)
                        lon_dict[str(p.longitude)] = longitudes.index(p.longitude)

                        # E então passa o valor para as variáveis que
                        # armazenarão o index.
                        i_lat = lat_dict[str(p.latitude)]
                        i_lon = lon_dict[str(p.longitude)]
                    except ValueError:
                        log_file.write(str(p.latitude) + ', ' + str(p.longitude))
                        continue

                # Iterar para cada dia do ano para o pixel corrente
                for i_time, t in enumerate(time):
                    val_u10 = 0
                    val_v10 = 0
                    val_t2m = 0
                    # val_slhf = 0
                    # val_sshf = 0
                    # val_e = 0
                    val_tp = 0

                    # Calcula a média diária, uma vez que o dataset
                    # vem com os valores de cada hora do dia.
                    for i_hour in range(24):

                        new_u10 = u10[i_time][i_hour][i_lat][i_lon]
                        new_v10 = v10[i_time][i_hour][i_lat][i_lon]
                        new_t2m = t2m[i_time][i_hour][i_lat][i_lon]
                        # new_slhf = slhf[i_time][i_hour][i_lat][i_lon]
                        # new_sshf = sshf[i_time][i_hour][i_lat][i_lon]
                        # new_e = e[i_time][i_hour][i_lat][i_lon]
                        new_tp = tp[i_time][i_hour][i_lat][i_lon]
                        
                        val_u10 += 0 if math.isnan(new_u10) else new_u10
                        val_v10 += 0 if math.isnan(new_v10) else new_v10
                        val_t2m += 0 if math.isnan(new_t2m) else new_t2m
                        # val_slhf += 0 if math.isnan(new_slhf) else new_slhf
                        # val_sshf += 0 if math.isnan(new_sshf) else new_sshf
                        # val_e += 0 if math.isnan(new_e) else new_e
                        val_tp += 0 if math.isnan(new_tp) else new_tp

                    pixel_data = {
                        'date': pandas.to_datetime(time[i_time]).date().strftime('%Y-%m-%d'),
                        'time_interval': 'diário',
                        'latitude': p.latitude,
                        'longitude': p.longitude,
                        'resolution': 0.1,
                        'data_model_name': 'ERA5',
                        'u10': val_u10 / 24, # Valores divididos por 24 para obter a média aritmética.
                        'v10': val_v10 / 24,
                        'tp2m': (val_t2m / 24) - 273.15,
                        # 'slhf': val_slhf / 24,
                        # 'sshf': val_sshf / 24,
                        # 'evapo': val_e / 24,
                        'precip': val_tp * 1000
                    }

                    print(pandas.to_datetime(time[i_time]).date().strftime('%d/%m/%Y'))

                    data_list.append(pixel_data)

                headers = {'content-type': 'application/json'}
                response = requests.post(url, data=json.dumps(data_list), headers=headers, verify=False)

                if response.status_code == 201:
                    # print(str(response.status_code) + ': ' + str(p.latitude) + ', ' + str(p.longitude) + ' - ' + date.strftime('%m/%Y'))
                    print(str(reesponse.status_code))
                else:
                    print(response.content)
                    # log_file.write(str(p.latitude) + ', ' + str(p.longitude) + ' -- ' + date.strftime('%d/%m/%Y'))

            curDate = pandas.to_datetime(time[-1]) + datetime.timedelta(days=1)

        print('Data final alcançada. Finalizar.')
        log_file.close()









