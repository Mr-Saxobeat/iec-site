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
        defaults= {
            'init': 'maxTemp',
            'unit': 'ºC',
            'chartType': 'line',
            'chartColor': 'red',
        }
    )

    minTemp, created = ElementVariable.objects.get_or_create(
        name = 'temperatura mínima',
        defaults= {
            'init': 'minTemp',
            'unit': 'ºC',
            'chartType': 'line',
            'chartColor': 'blue',
        }
    )

    solarIns, created = ElementVariable.objects.get_or_create(
        name = 'radiação solar',
        defaults = {
            'init': 'solarIns',
            'unit': 'MJ/m²',
            'chartType': 'line',
            'chartColor': 'red',
        }
    )

    relHum, created = ElementVariable.objects.get_or_create(
        name = 'umidade relativa',
        defaults = {
            'init': 'relHum',
            'unit': '%',
            'chartType': 'bar',
            'chartColor': 'blue',
        }
    )
    relHum.chartType = 'bar'
    relHum.chartColor = 'blue'
    relHum.save()

    windSpeed, created = ElementVariable.objects.get_or_create(
        name = 'velocidade do vento',
        defaults = {
            'init': 'windSpeed',
            'unit': 'm/s',
            'chartType': 'line',
            'chartColor': 'black',
        }
    )
    windSpeed.chartType = 'line'
    windSpeed.chartColor = 'black'
    windSpeed.save()

    evapo_mm, created = ElementVariable.objects.get_or_create(
        name = 'evapotranspiração',
        init = 'evapo_mm',
        defaults = {
            'init': 'evapo_mm',
            'unit': 'mm',
            'chartType': 'bar',
            'chartColor': 'blue',
        }
    )
    evapo_mm.unit = 'mm'
    evapo_mm.chartType = 'bar'
    evapo_mm.chartColor = 'blue'
    evapo_mm.save()

    evapo_m, created = ElementVariable.objects.get_or_create(
        name = 'evapotranspiração_m',
        init = 'evapo_m',
        defaults = {
            'init': 'evapo_m',
            'unit': 'm',
            'chartType': 'bar',
            'chartColor': 'blue',
        }
    )
    evapo_m.unit = 'm'
    evapo_m.chartType = 'bar'
    evapo_m.chartColor = 'blue'
    evapo_m.save()

    precip, created = ElementVariable.objects.get_or_create(
        name = 'precipitação',
        defaults = {
            'init': 'precip',
            'unit': 'mm',
            'chartType': 'bar',
            'chartColor': 'blue',
        }
    )
    precip.unit = 'mm'
    precip.chartType = 'bar'
    precip.chartColor = 'blue'
    precip.save()

    flow, created = ElementVariable.objects.get_or_create(
        name = 'vazão',
        defaults = {
            'init': 'flow',
            'unit': 'm³/s',
            'chartType': 'line',
            'chartColor': 'blue',
        }
    )
    flow.unit = 'm³/s'
    flow.chartType = 'line'
    flow.chartColor = 'blue'
    flow.save()

    xavier, created = ElementSource.objects.get_or_create(
        name = 'xavier',
        category = ElementCategory.objects.get(name='observados'),
    )
    xavier.variables.add(maxTemp, minTemp, solarIns, relHum, windSpeed, evapo_mm)
    xavier.name = "Xavier Et al"
    xavier.save()

    inmet, created = ElementSource.objects.get_or_create(
        name = 'inmet',
        category = ElementCategory.objects.get(name='observados'),
    )
    inmet.variables.add(maxTemp, minTemp, relHum, precip)
    inmet.name = "INMET"
    inmet.save()

    ana, created = ElementSource.objects.get_or_create(
        name = 'ana',
        category = ElementCategory.objects.get(name='observados'),
    )
    ana.variables.add(precip, flow)
    ana.name = "ANA"
    ana.save()
