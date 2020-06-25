from django.shortcuts import render

def IndexView(request):
    return render(request, 'home/index.html')
