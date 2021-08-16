from django.contrib import admin

from .models import Region, Sample, SampleMetaData

class RegionAdmin(admin.ModelAdmin):
    ordering = ['localizacion','cp']
    search_fields = ['localizacion','cp','division','pais']
    l = [f.name for f in Region._meta.get_fields()]
    l.remove('sample')
    list_display = l
    list_editable = ['latitud', 'longitud', 'localizacion_org']
    list_filter = ('localizacion',)

class SampleAdmin(admin.ModelAdmin):
    ordering = ['id_uvigo']
    search_fields = ['id_uvigo']
    list_display = [f.name for f in Sample._meta.fields]
    list_filter = ('categoria_muestra','vigilancia','samplemetadata__vacunacion_tipo','samplemetadata__id_hospital')

class SampleMetaDataAdmin(admin.ModelAdmin):
    ordering = ['id_uvigo_id__id_uvigo']
    search_fields = ['id_uvigo_id__id_uvigo']
    list_display = [f.name for f in SampleMetaData._meta.fields]

admin.site.register(Region, RegionAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(SampleMetaData, SampleMetaDataAdmin)
