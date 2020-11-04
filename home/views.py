from django.shortcuts import render
from vismet.models import ElementCategory

def IndexView(request):
    observados = ElementCategory.objects.get(name='observados')
    reanalise = ElementCategory.objects.get(name='reanálise')
    simulados = ElementCategory.objects.get(name='simulados')
    return render(request, 'home/index.html', {'observados': observados, 'reanalise': reanalise, 'simulados': simulados})
