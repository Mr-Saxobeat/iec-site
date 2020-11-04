from django.contrib import admin
from vismet.models import ElementCategory, ElementVariable, DataModel, ElementSource, Station

admin.site.register(ElementCategory)
admin.site.register(ElementVariable)
admin.site.register(ElementSource)
admin.site.register(Station)
