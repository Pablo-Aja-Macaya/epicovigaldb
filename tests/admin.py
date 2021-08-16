from django.contrib import admin
import csv
from django.http import HttpResponse

# Register your models here.
from .models import SingleCheckTest, NGSstatsTest, NextcladeTest
from .models import LineagesTest#, LineagesMostCommonCountries
from .models import VariantsTest
from .models import PicardTest


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


class PicardTestAdmin(admin.ModelAdmin, ExportCsvMixin):
    ordering = ['date']
    search_fields = ['id_uvigo_id__id_uvigo']
    list_display = [f.name for f in PicardTest._meta.get_fields()]
    list_filter = ('id_uvigo_id__samplemetadata__id_hospital',)
    actions = ["export_as_csv"]

class NGSstatsTestAdmin(admin.ModelAdmin, ExportCsvMixin):
    ordering = ['date']
    search_fields = ['id_uvigo_id__id_uvigo']
    list_display = [f.name for f in NGSstatsTest._meta.get_fields()]
    list_filter = ('id_uvigo_id__samplemetadata__id_hospital',)
    actions = ["export_as_csv"]

class NextcladeTestAdmin(admin.ModelAdmin, ExportCsvMixin):
    ordering = ['date']
    search_fields = ['id_uvigo_id__id_uvigo']
    list_display = [f.name for f in NextcladeTest._meta.get_fields()]
    list_filter = ('id_uvigo_id__samplemetadata__id_hospital','clade',
                    'qc_private_mutations_status','qc_missing_data_status','qc_snp_clusters_status',
                    'qc_mixed_sites_status','qc_overall_status','qc_frameshifts_status','qc_stopcodons_status')
    actions = ["export_as_csv"]

class VariantsTestAdmin(admin.ModelAdmin):
    ordering = ['date']
    search_fields = ['id_uvigo_id__id_uvigo']
    list_display = [f.name for f in VariantsTest._meta.get_fields()]
    list_filter = ('id_uvigo_id__samplemetadata__id_hospital',)
    actions = ["export_as_csv"]

class LineagesTestAdmin(admin.ModelAdmin, ExportCsvMixin):
    ordering = ['date']
    search_fields = ['id_uvigo_id__id_uvigo']
    l = [f.name for f in LineagesTest._meta.get_fields()]
    l.remove('most_common_countries')
    list_display = l
    list_filter = ('id_uvigo_id__samplemetadata__id_hospital','lineage')
    actions = ["export_as_csv"]

admin.site.register(PicardTest, PicardTestAdmin)
# admin.site.register(SingleCheckTest)
admin.site.register(NGSstatsTest, NGSstatsTestAdmin)
admin.site.register(NextcladeTest, NextcladeTestAdmin)
admin.site.register(VariantsTest, VariantsTestAdmin)
admin.site.register(LineagesTest, LineagesTestAdmin)
# admin.site.register(LineagesMostCommonCountries)