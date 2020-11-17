import netCDF4 as nc
import glob
import datetime
from vismet.models import DataModel, ElementSource, Pixel, PixelData, ElementCategory, ElementVariable

def run(path='/home/weiglas/Documents/iec/dados/3. Dados de Cenários Futuros/novo-netcdf-eta/NetCDF --- Eta 5km HadGEM2-ES-20201111T141546Z-001/NetCDF --- Eta 5km HadGEM2-ES/Mensal/EVTP/RCP 4.5/EtaHADGEM2_5km_EVTP_RCP4.5_2006-2040.nc',
        rm=0):

    model_name = 'RCP 4.5, 5Km'
    data_model, created = DataModel.objects.get_or_create(name=model_name)

    eCategory, created = ElementCategory.objects.get_or_create(name='simulados')

    eSource, created = ElementSource.objects.get_or_create(
        display_name='ETA Por Pixels',
        name='eta por pixel',
        category=eCategory,
        )

    eSourcr.data_model.add(data_model)
    eSource.variables.add(eVar)
    eSource.save()

    eVar, created = ElementVariable.objects.get_or_create(
        name = 'evapotranspiração',
        init = 'evapo',
        unit = 'mm',
        chartType = 'bar',
        chartColor = 'blue',
    )


    evapo_ds = nc.Dataset(path)

    list_latitudes = evapo_ds['lat'][:].data.tolist()
    round_latitudes = []
    for lat in list_latitudes:
        round_latitudes.append(round(lat, 2))

    list_longitudes = evapo_ds['lon'][:].data.tolist()
    round_longitudes = []
    for lon in list_longitudes:
        round_longitudes.append(round(lon, 2))

    time_len = len(evapo_ds['time'][:].data.tolist())
    year = 2006
    month = 1
    pixels = Pixel.objects.all()

    for i_time in range(time_len):
        month = month + i_time

        if rm != 0:
            if month == rm:
                print("ACABOU RUN_MONTH")
                return 0

        if (month % 12 != 0):
            date = datetime.date(year, month % 12, 1)
        else:
            date = datetime.date(year, 12, 1)
            year = year + 1

        for px in pixels:
            try:
                i_lat = round_latitudes.index(px.latitude)
                i_lon = round_longitudes.index(px.longitude)
                pixel_data, created = PixelData.objects.get_or_create(
                                        pixel = px,
                                        data_model = data_model,
                                        date = date,
                                        evapo = evapo_ds['evtp'][i_time, i_lat, i_lon].data.tolist()
                                        )
                print(pixel_data)

            except ValueError:
                raise ValueError
    print("FIM")
