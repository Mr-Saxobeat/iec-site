from vismet.models import ElementCategory, ElementSource, ElementVariable

def LoadCategories():
    ElementCategory.objects.get_or_create(
        name = 'observados',
    )

    ElementCategory.objects.get_or_create(
        name = 'reanálise',
    )

    ElementCategory.objects.get_or_create(
        name = 'simulados',
    )

    maxTemp, created = ElementVariable.objects.get_or_create(
        name = 'temperatura máxima',
        init = 'maxTemp',
        unit = 'ºC',
        chartType = 'line',
        chartColor = 'red',
    )

    minTemp, created = ElementVariable.objects.get_or_create(
        name = 'temperatura mínima',
        init = 'minTemp',
        unit = 'ºC',
        chartType = 'line',
        chartColor = 'blue',
    )

    solarIns, created = ElementVariable.objects.get_or_create(
        name = 'radiação solar',
        init = 'solarIns',
        unit = 'MJ/m²',
        chartType = 'line',
        chartColor = 'red',
    )

    relHum, created = ElementVariable.objects.get_or_create(
        name = 'umidade relativa',
        init = 'relHum',
        unit = '%',
        chartType = 'line',
        chartColor = 'red',
    )

    windSpeed, created = ElementVariable.objects.get_or_create(
        name = 'velocidade do vento',
        init = 'windSpeed',
        unit = 'm/s',
        chartType = 'line',
        chartColor = 'red',
    )

    evapo, created = ElementVariable.objects.get_or_create(
        name = 'evapotranspiração',
        init = 'evapo',
        unit = 'mm³',
        chartType = 'line',
        chartColor = 'red',
    )

    precip, created = ElementVariable.objects.get_or_create(
        name = 'precipitação',
        init = 'precip',
        unit = 'mm³',
        chartType = 'bar',
        chartColor = 'blue',
    )

    flow, created = ElementVariable.objects.get_or_create(
        name = 'vazão',
        init = 'flow',
        unit = 'mm³/s',
        chartType = 'bar',
        chartColor = 'blue',
    )

    xavier, created = ElementSource.objects.get_or_create(
        name = 'xavier',
        category = ElementCategory.objects.get(name='observados'),
    )
    xavier.variables.add(maxTemp, minTemp, solarIns, relHum, windSpeed, evapo)
    xavier.save()

    inmet, created = ElementSource.objects.get_or_create(
        name = 'inmet',
        category = ElementCategory.objects.get(name='observados'),
    )
    inmet.variables.add(maxTemp, minTemp, relHum, precip)
    inmet.save()

    ana, created = ElementSource.objects.get_or_create(
        name = 'ana',
        category = ElementCategory.objects.get(name='observados'),
    )
    ana.variables.add(precip, flow)
    ana.save()
