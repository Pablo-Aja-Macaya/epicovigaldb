from django.contrib import admin

# Register your models here.
from .models import SingleCheckTest, NGSstatsTest, NextcladeTest
from .models import LineagesTest#, LineagesMostCommonCountries
from .models import VariantsTest
from .models import PicardTest

class PicardTestAdmin(admin.ModelAdmin):
    ordering = ['date']
    search_fields = ['id_uvigo_id__id_uvigo']
    list_display = [f.name for f in PicardTest._meta.get_fields()]

    list_filter = ('id_uvigo_id__samplemetadata__id_hospital',)

class NGSstatsTestAdmin(admin.ModelAdmin):
    ordering = ['date']
    search_fields = ['id_uvigo_id__id_uvigo']
    list_display = [f.name for f in NGSstatsTest._meta.get_fields()]

    list_filter = ('id_uvigo_id__samplemetadata__id_hospital',)

class NextcladeTestAdmin(admin.ModelAdmin):
    ordering = ['date']
    search_fields = ['id_uvigo_id__id_uvigo']
    list_display = [f.name for f in NextcladeTest._meta.get_fields()]

    list_filter = ('id_uvigo_id__samplemetadata__id_hospital','clade',
                    'qc_private_mutations_status','qc_missing_data_status','qc_snp_clusters_status',
                    'qc_mixed_sites_status','qc_overall_status','qc_frameshifts_status','qc_stopcodons_status')

class VariantsTestAdmin(admin.ModelAdmin):
    ordering = ['date']
    search_fields = ['id_uvigo_id__id_uvigo']
    list_display = [f.name for f in VariantsTest._meta.get_fields()]

    list_filter = ('id_uvigo_id__samplemetadata__id_hospital',)

class LineagesTestAdmin(admin.ModelAdmin):
    ordering = ['date']
    search_fields = ['id_uvigo_id__id_uvigo']
    
    l = [f.name for f in LineagesTest._meta.get_fields()]
    l.remove('most_common_countries')
    list_display = l

    list_filter = ('id_uvigo_id__samplemetadata__id_hospital','lineage')

admin.site.register(PicardTest, PicardTestAdmin)
# admin.site.register(SingleCheckTest)
admin.site.register(NGSstatsTest, NGSstatsTestAdmin)
admin.site.register(NextcladeTest, NextcladeTestAdmin)
admin.site.register(VariantsTest, VariantsTestAdmin)
admin.site.register(LineagesTest, LineagesTestAdmin)
# admin.site.register(LineagesMostCommonCountries)