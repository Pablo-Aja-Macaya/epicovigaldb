from django.contrib import admin
import csv
from django.http import HttpResponse

from .models import Region, Sample, SampleMetaData


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

class RegionAdmin(admin.ModelAdmin, ExportCsvMixin):
    ordering = ['localizacion','cp']
    search_fields = ['localizacion','cp','division','pais']
    l = [f.name for f in Region._meta.get_fields()]
    l.remove('sample')
    list_display = l
    list_editable = ['latitud', 'longitud', 'localizacion_org']
    list_filter = ('localizacion',)
    actions = ["export_as_csv"]

class SampleAdmin(admin.ModelAdmin, ExportCsvMixin):
    ordering = ['id_uvigo']
    search_fields = ['id_uvigo']
    list_display = [f.name for f in Sample._meta.fields]
    list_filter = ('categoria_muestra','vigilancia','samplemetadata__vacunacion_tipo','samplemetadata__id_hospital')
    actions = ["export_as_csv"]

class SampleMetaDataAdmin(admin.ModelAdmin, ExportCsvMixin):
    ordering = ['id_uvigo_id__id_uvigo']
    search_fields = ['id_uvigo_id__id_uvigo']
    list_display = [f.name for f in SampleMetaData._meta.fields]
    actions = ["export_as_csv"]

admin.site.register(Region, RegionAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(SampleMetaData, SampleMetaDataAdmin)
