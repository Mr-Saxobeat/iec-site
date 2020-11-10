from django.contrib import admin
from vismet.models import ElementCategory, ElementVariable, DataModel, ElementSource, SubSource, Station

class ElementCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name', 'desc')
    fields = ('display_name', 'desc', 'subsource')

class SubSourceAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'desc', 'time_interval')
    fields = ('display_name', 'desc', 'time_interval', 'related_source')

admin.site.register(ElementCategory, ElementCategoryAdmin)
admin.site.register(SubSource, SubSourceAdmin)
admin.site.register(ElementVariable)
admin.site.register(ElementSource)
admin.site.register(Station)
