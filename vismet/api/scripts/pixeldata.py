import os
import requests
import netCDF4 as nc
import datetime
from vismet.models import DataModel, Pixel, PixelData


def incrementMonth(date):
    if date.month < 12:
        return datetime.date(date.year, date.month + 1, 1)
    else:
        return datetime.date(date.year + 1, 1, 1)

def round_dot_zero_five(value):
    return round(0.05 * round(value / 0.05), 2)

def run(url='http://127.0.0.1:8000/api2/pixeldata/',
        base_dir='/home/weiglas/Documents/iec/dados/reanalise/'):

    file_dir = os.path.join(base_dir, 'chirps.AS.1981-2010.mon.nc')

    ds = nc.Dataset(file_dir)

    # Arredonda o valor das latitudes
    list_latitudes = ds['lat'][:].data.tolist()
    round_latitudes = []
    for lat in list_latitudes:
        round_latitudes.append(round_dot_zero_five(lat))

    # Arredonda o valor das longitudes
    list_longitudes = ds['lon'][:].data.tolist()
    round_longitudes = []
    for lon in list_longitudes:
        round_longitudes.append(round_dot_zero_five(lon))

    pixels = Pixel.objects.all()
    time_len = ds['time'].shape[0]

    for pixel in pixels:
        try:
            i_lat = round_latitudes.index(pixel.latitude)
        except ValueError:
            print('A latitude não existe na lista: ' + str(pixel.latitude))
            continue

        try:
            i_lon = round_longitudes.index(pixel.longitude)
        except ValueError:
            print('A longitude não existe na lista: ' + str(pixel.longitude))
            continue

        date = datetime.date(1981, 1, 1)
        for i_time in range(time_len):
            
            precip = ds['precip'][i_time, i_lat, i_lon].tolist()

            data = {
                'latitude': pixel.latitude,
                'longitude': pixel.longitude,
                'data_model_name': data_model.name,
                'date': date.strftime('%Y-%m-%d'),
                'precip': precip
            }

            r = requests.post(url, data=data, verify=False)

            if r.status_code == 201:
                print(str(pixel.latitude) + ' ' + str(pixel.longitude) + ' -- ' + date.strftime('%d/%m/%Y'))
            else:
                print(r.text)

            date = incrementMonth(date)

            if date.year > 1981:
                print('Vamo acabar por aqui')
                return 0





        