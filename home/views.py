from django.shortcuts import render
from vismet.models import ElementCategory

def IndexView(request):
    categories = ElementCategory.objects.all().order_by('pk')
    return render(request, 'home/index.html', {'categories': categories})
