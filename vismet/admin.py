from django.contrib import admin
from vismet.models import ElementCategory, ElementVariable, DataModel, ElementSource, Station

class ElementCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name', 'desc')
    fields = ('display_name', 'desc')

admin.site.register(ElementCategory, ElementCategoryAdmin)
admin.site.register(ElementVariable)
admin.site.register(ElementSource)
admin.site.register(Station)
