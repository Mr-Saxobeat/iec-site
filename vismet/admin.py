from django.contrib import admin
from django.contrib.gis import admin as geoadmin
from vismet.models import Station, ElementCategory, ElementVariable, DataModel, ElementSource, SubSource, SubSourceDetail

class ElementCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name', 'desc')
    fields = ('display_name', 'desc')

class SubSourceAdmin(admin.ModelAdmin):
    list_display = ('display_name',)

class SubSourceDetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'text')

class ElementSourceAdmin(admin.ModelAdmin):
    list_display = ('display_name',)

class StationAdmin(geoadmin.OSMGeoAdmin):
    fields = (
                'source',
                'omm_code',
                'inmet_code',
                'state',
                'city',
                'type',
                'altitude',
                'startDate',
                'finalDate',
                'status',
                )

admin.site.register(ElementCategory, ElementCategoryAdmin)
admin.site.register(SubSource, SubSourceAdmin)
admin.site.register(SubSourceDetail, SubSourceDetailAdmin)
admin.site.register(ElementVariable)
admin.site.register(ElementSource, ElementSourceAdmin)
admin.site.register(Station, StationAdmin)
