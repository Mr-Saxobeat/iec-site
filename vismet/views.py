from django.shortcuts import render

def VisMetView(request):
    return render(request, 'vismet/vismet.html')
