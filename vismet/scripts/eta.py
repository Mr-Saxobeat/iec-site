import netCDF4 as nc
import glob
import datetime
from vismet.models import DataModel, ElementSource, Pixel, PixelData, ElementCategory, ElementVariable

def run(path='/home/weiglas/Documents/iec/dados/3. Dados de Cenários Futuros/eta-correto/historico/',
        rm=0, year=0):

    if year == 0:
        print("Configure o ano inicial e tente novamente.")
        return 0

    model_name = 'Histórico, 5Km'
    data_model, created = DataModel.objects.get_or_create(name=model_name)

    eCategory, created = ElementCategory.objects.get_or_create(name='simulados')

    eSource, source_created = ElementSource.objects.get_or_create(
        name='eta por pixel',
        category=eCategory,
        )

    evapo, created = ElementVariable.objects.get_or_create(
    init = 'evapo_mm',
    defaults = {
        'name': 'evapotranspiração',
        'unit': 'mm',
        'chartType': 'line',
        'chartColor': 'red',
        }
    )

    minTemp, created = ElementVariable.objects.get_or_create(
    init = 'minTemp',
    defaults = {
        'name': 'temperatura mínima',
        'unit': 'ºC',
        'chartType': 'line',
        'chartColor': 'blue',
        }
    )

    maxTemp, created = ElementVariable.objects.get_or_create(
        init = 'maxTemp',
        defaults = {
            'name': 'temperatura máxima',
            'unit': 'ºC',
            'chartType': 'line',
            'chartColor': 'red',
        }
    )

    ocis, created = ElementVariable.objects.get_or_create(
        init = 'ocis',
        defaults = {
            'name': 'radiação de onda curta incidente à superficie',
            'unit': 'W/m²',
            'chartType': 'line',
            'chartColor': 'red',
        }
    )

    precip, created = ElementVariable.objects.get_or_create(
        init = 'precip',
        defaults = {
            'name': 'precipitação',
            'unit': 'mm',
            'chartType': 'bar',
            'chartColor': 'blue',
        }
    )

    rnof, created = ElementVariable.objects.get_or_create(
        init = 'rnof',
        defaults = {
            'name': 'escoamento superficial',
            'unit': 'mm',
            'chartType': 'bar',
            'chartColor': 'blue',
        }
    )

    tp2m, created = ElementVariable.objects.get_or_create(
        init = 'tp2m',
        defaults = {
            'name': 'temperatura a 2m da superfície',
            'unit': 'ºC',
            'chartType': 'line',
            'chartColor': 'black',
        }
    )

    eSource.data_model.add(data_model)
    eSource.variables.add(evapo, minTemp, maxTemp, ocis, precip, rnof, tp2m)
    eSource.save()

    evapo_ds = nc.Dataset(path + 'EVTP_Historical.nc')
    minTemp_ds = nc.Dataset(path + 'MNTP_Historical.nc')
    maxTemp_ds = nc.Dataset(path + 'MXTP_Historical.nc')
    ocis_ds = nc.Dataset(path + 'OCIS_Historical.nc')
    precip_ds = nc.Dataset(path + 'PREC_Historical.nc')
    rnof_ds = nc.Dataset(path + 'RNOF_Historical.nc')
    tp2m_ds = nc.Dataset(path + 'TP2M_Historical.nc')

    # Arredonda o valor das latitudes
    list_latitudes = evapo_ds['lat'][:].data.tolist()
    round_latitudes = []
    for lat in list_latitudes:
        round_latitudes.append(round(lat, 2))

    # Arredonda o valor das longitudestguh6
    list_longitudes = evapo_ds['lon'][:].data.tolist()
    round_longitudes = []
    for lon in list_longitudes:
        round_longitudes.append(round(lon, 2))

    time_len = len(evapo_ds['time'][:].data.tolist())
    pixels = Pixel.objects.all()

    for i_time in range(time_len):
        month = i_time + 1

        if rm != 0:
            if month == rm:
                print("ACABOU RUN_MONTH")
                return 0

        if month % 12 != 0:
            date = datetime.date(year, month % 12, 1)

        else:
            date = datetime.date(year, 12, 1)
            year = year + 1
            print(" ")

        print(date.strftime("%m/%Y"), end = " ")

        for px in pixels:
            try:
                pixel_data = PixelData.objects.get(pixel=px, date=date)
                continue
            except PixelData.DoesNotExist:
                try:
                    i_lat = round_latitudes.index(px.latitude)
                    i_lon = round_longitudes.index(px.longitude)
                    pixel_data, created = PixelData.objects.get_or_create(
                                            pixel = px,
                                            data_model = data_model,
                                            date = date,
                                            defaults = {
                                                'evapo': evapo_ds['evtp'][i_time, i_lat, i_lon].data.tolist(),
                                                'minTemp': minTemp_ds['mntp'][i_time, i_lat, i_lon].data.tolist(),
                                                'maxTemp': maxTemp_ds['mxtp'][i_time, i_lat, i_lon].data.tolist(),
                                                'ocis': ocis_ds['ocis'][i_time, i_lat, i_lon].data.tolist(),
                                                'precip': precip_ds['prec'][i_time, i_lat, i_lon].data.tolist(),
                                                'rnof': rnof_ds['rnof'][i_time, i_lat, i_lon].data.tolist(),
                                                'tp2m': tp2m_ds['tp2m'][i_time, i_lat, i_lon].data.tolist(),
                                                }
                                            )

                except ValueError:
                    raise ValueError
    print("FIM")
