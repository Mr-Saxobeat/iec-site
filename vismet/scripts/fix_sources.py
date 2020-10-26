from vismet.models import ElementSource

def run():
    ana = ElementSource.objects.get(name='ana')
    inmet = ElementSource.objects.get(name='inmet')
    xavier = ElementSource.objects.get(name='xavier')

    ana.variables = [
        ['precipitação', 'mm³'],
        ['vazão', 'm³/s'],
    ]
    ana.save()

    inmet.variables = [
        ['temperatura máxima', 'ºC'],
        ['temperatura mínima', 'ºC'],
        ['umidade relativa', '%'],
        ['precipitação', 'mm³']
    ]
    inmet.save()

    xavier.variables = [
        ['temperatura máxima', 'ºC'],
        ['temperatura mínima', 'ºC'],
        ['radiação solar', 'MJ/m²'],
        ['umidade relativa', '%'],
        ['velocidade do vento', 'm/s'],
        ['evapotranspiração', 'mm'],
    ]
    xavier.save()
