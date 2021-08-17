from django.db import models
from django import forms
from django.db.models.base import Model
from django.forms import ModelForm
from upload.models import Sample, Region
from upload.models import SampleMetaData
from tests.models import PicardTest, NextcladeTest, NGSstatsTest, SingleCheckTest, VariantsTest
from tests.models import LineagesTest

import django_tables2 as tables
import django_filters
from django_tables2.utils import A
# Create your models here.

# In[1]: Tablas de metadatos
class SampleTable(tables.Table):
    id_uvigo = tables.LinkColumn('specific_sample', args=[A('id_uvigo')])
    fecha_muestra = tables.DateTimeColumn(format ='d/m/Y')
    class Meta:
        model = Sample
        template_name = "table_template.html"

class RegionTable(tables.Table):
    id_region = tables.LinkColumn('specific_region', args=[A('id_region')])
    class Meta:
        model = Region
        template_name = "table_template.html"

class SampleMetaDataTable(tables.Table):
    id_uvigo = tables.LinkColumn('specific_sample', args=[A('id_uvigo')])
    fecha_envio_cdna = tables.DateTimeColumn(format ='d/m/Y')
    fecha_run_ngs = tables.DateTimeColumn(format ='d/m/Y')
    fecha_entrada_fastq = tables.DateTimeColumn(format ='d/m/Y')
    fecha_sintomas = tables.DateTimeColumn(format ='d/m/Y')
    fecha_diagnostico = tables.DateTimeColumn(format ='d/m/Y')
    fecha_entrada = tables.DateTimeColumn(format ='d/m/Y')
    class Meta:
        model = SampleMetaData
        template_name = "table_template.html"

# In[2]: Tablas de resultados
class LineagesTable(tables.Table):
    id_uvigo = tables.LinkColumn('specific_sample', args=[A('id_uvigo')])
    date = tables.DateTimeColumn(format ='d/m/Y, h:i A')
    most_common_countries = tables.ManyToManyColumn()
    class Meta:
        model = LineagesTest
        template_name = "table_template.html"

class PicardTable(tables.Table):
    id_uvigo = tables.LinkColumn('specific_sample', args=[A('id_uvigo')])
    date = tables.DateTimeColumn(format ='d/m/Y, h:i A')
    class Meta:
        model = PicardTest
        template_name = "table_template.html"
        
class NextcladeTable(tables.Table):
    id_uvigo = tables.LinkColumn('specific_sample', args=[A('id_uvigo')])
    date = tables.DateTimeColumn(format ='d/m/Y, h:i A')
    class Meta:
        model = NextcladeTest
        template_name = "table_template.html"

class NGSTable(tables.Table):
    id_uvigo = tables.LinkColumn('specific_sample', args=[A('id_uvigo')])
    date = tables.DateTimeColumn(format ='d/m/Y, h:i A')
    class Meta:
        model = NGSstatsTest
        template_name = "table_template.html"

class VariantsTable(tables.Table):
    id_uvigo = tables.LinkColumn('specific_sample', args=[A('id_uvigo')])
    date = tables.DateTimeColumn(format ='d/m/Y, h:i A')
    class Meta:
        model = VariantsTest
        template_name = "table_template.html"

class SingleCheckTable(tables.Table):
    id_uvigo = tables.LinkColumn('specific_sample', args=[A('id_uvigo')])
    date = tables.DateTimeColumn(format ='d/m/Y, h:i A')
    class Meta:
        model = SingleCheckTest
        template_name = "table_template.html"


# In[3]: Tabla de tests completados
class CompletedTestsTable(tables.Table):
    # Tabla donde se indicará para cada muestra qué tests tiene hechos
    id_uvigo = tables.LinkColumn('specific_sample', args=[A('id_uvigo')])
    picardtest = tables.Column(verbose_name='Picard')
    nextcladetest = tables.Column(verbose_name='NextClade')
    ngsstatstest = tables.Column(verbose_name='NGSStats')
    lineagestest = tables.Column(verbose_name='Pangolin')
    singlechecktest = tables.Column(verbose_name='SingleCheck')
    variantstest__id_uvigo = tables.Column(verbose_name='iVar')
    class Meta:
        template_name = "table_template.html"


# In[4]: Filtros
class SampleFilter(django_filters.FilterSet):
    obj = Sample.objects.values('categoria_muestra','vigilancia','nodo_secuenciacion')
    choices_categoria = [(i,i) for i in obj.values_list('categoria_muestra',flat=True).distinct().order_by('categoria_muestra') if i]
    choices_vigilancia = [(i,i) for i in obj.values_list('vigilancia',flat=True).distinct().order_by('vigilancia') if i]
    choices_nodos = [(i,i) for i in obj.values_list('nodo_secuenciacion',flat=True).distinct().order_by('nodo_secuenciacion') if i]
    choices_hospitales = [(i,i) for i in SampleMetaData.objects.values_list('id_hospital',flat=True).distinct().order_by('id_hospital') if i]
    
    id_uvigo = django_filters.CharFilter(field_name = 'id_uvigo', lookup_expr='icontains')
    categoria_muestra = django_filters.MultipleChoiceFilter(choices=choices_categoria, widget=forms.CheckboxSelectMultiple(attrs={'class':'ul-no-bullets '}))
    vigilancia = django_filters.MultipleChoiceFilter(choices=choices_vigilancia, widget=forms.CheckboxSelectMultiple(attrs={'class':'ul-no-bullets '}))
    nodo_secuenciacion = django_filters.MultipleChoiceFilter(choices=choices_nodos, widget=forms.CheckboxSelectMultiple(attrs={'class':'ul-no-bullets '}))
    fecha_muestra = django_filters.DateFromToRangeFilter(field_name = 'fecha_muestra', widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'}))
    samplemetadata__id_hospital = django_filters.MultipleChoiceFilter(choices=choices_hospitales, label='Hospital', widget=forms.CheckboxSelectMultiple(attrs={'class':'ul-no-bullets '}))
    class Meta:
        model = Sample
        fields = ['id_uvigo', 'fecha_muestra', 'samplemetadata__id_hospital', 'vigilancia', 'categoria_muestra', 'nodo_secuenciacion']

class MetaDataFilter(django_filters.FilterSet):
    id_uvigo = django_filters.CharFilter(field_name = 'id_uvigo', lookup_expr='icontains')
    fecha_entrada = django_filters.DateFromToRangeFilter(field_name = 'fecha_entrada')

    class Meta:
        model = SampleMetaData
        fields = ['id_uvigo', 'fecha_entrada']

class RegionFilter(django_filters.FilterSet):
    id_region = django_filters.NumberFilter(field_name = 'id_region', lookup_expr='icontains')
    localizacion = django_filters.CharFilter(field_name = 'localizacion', lookup_expr='icontains')
    cp = django_filters.CharFilter(field_name = 'cp', lookup_expr='icontains')
    division = django_filters.CharFilter(field_name = 'division', lookup_expr='icontains')
    pais = django_filters.CharFilter(field_name = 'pais', lookup_expr='icontains')
    region = django_filters.CharFilter(field_name = 'region', lookup_expr='icontains')
    class Meta:
        model = Region
        fields = ['id_region','localizacion','cp','division']


class NextcladeFilter(django_filters.FilterSet):
    clade_choices = [(i,i) for i in NextcladeTest.objects.values_list('clade', flat=True).distinct().order_by('clade').exclude(clade='')]
    
    id_uvigo_id__id_uvigo = django_filters.CharFilter(field_name = 'id_uvigo_id__id_uvigo', lookup_expr='icontains')
    clade = django_filters.MultipleChoiceFilter(choices=clade_choices, widget=forms.CheckboxSelectMultiple(attrs={'class':'ul-no-bullets '}))
    class Meta:
        model = Sample
        fields = ['id_uvigo_id__id_uvigo']

class PangolinFilter(django_filters.FilterSet):
    lineage_choices = [(i,i) for i in LineagesTest.objects.values_list('lineage', flat=True).distinct().order_by('lineage').exclude(lineage='')]
    
    id_uvigo_id__id_uvigo = django_filters.CharFilter(field_name = 'id_uvigo_id__id_uvigo', lookup_expr='icontains')
    lineage = django_filters.MultipleChoiceFilter(choices=lineage_choices, widget=forms.CheckboxSelectMultiple(attrs={'class':'ul-no-bullets '}))
    class Meta:
        model = Sample
        fields = ['id_uvigo_id__id_uvigo']

class PicardFilter(django_filters.FilterSet):    
    id_uvigo_id__id_uvigo = django_filters.CharFilter(field_name = 'id_uvigo_id__id_uvigo', lookup_expr='icontains')
    mean_target_coverage = django_filters.RangeFilter()
    median_target_coverage = django_filters.RangeFilter()
    pct_target_bases_1x = django_filters.RangeFilter()
    pct_target_bases_10x = django_filters.RangeFilter()
    pct_target_bases_100x = django_filters.RangeFilter()
    class Meta:
        model = Sample
        fields = ['id_uvigo_id__id_uvigo']

class NGSFilter(django_filters.FilterSet):    
    id_uvigo_id__id_uvigo = django_filters.CharFilter(field_name = 'id_uvigo_id__id_uvigo', lookup_expr='icontains')
    total_reads = django_filters.RangeFilter()
    mapped = django_filters.RangeFilter()
    trimmed = django_filters.RangeFilter()
    class Meta:
        model = Sample
        fields = ['id_uvigo_id__id_uvigo']

class VariantsFilter(django_filters.FilterSet):
    # ref_choices = [(i,i) for i in VariantsTest.objects.values_list('ref', flat=True).distinct().order_by('ref').exclude(ref='')]
    # alt_choices = [(i,i) for i in VariantsTest.objects.values_list('alt', flat=True).distinct().order_by('alt').exclude(ref='')]
    ref_aa_choices = [(i,i) for i in VariantsTest.objects.values_list('ref_aa', flat=True).distinct().order_by('ref_aa').exclude(ref='')]
    alt_aa_choices = [(i,i) for i in VariantsTest.objects.values_list('alt_aa', flat=True).distinct().order_by('alt_aa').exclude(ref='')]
    # ref_codon_choices = [(i,i) for i in VariantsTest.objects.values_list('ref_codon', flat=True).distinct().order_by('ref_codon').exclude(ref='')]
    # alt_codon_choices = [(i,i) for i in VariantsTest.objects.values_list('alt_codon', flat=True).distinct().order_by('alt_codon').exclude(ref='')]

    id_uvigo_id__id_uvigo = django_filters.CharFilter(field_name = 'id_uvigo_id__id_uvigo', lookup_expr='icontains')
    pos = django_filters.RangeFilter()
    ref_aa = django_filters.MultipleChoiceFilter(choices=ref_aa_choices, widget=forms.CheckboxSelectMultiple(attrs={'class':'ul-no-bullets '}))
    alt_aa = django_filters.MultipleChoiceFilter(choices=alt_aa_choices, widget=forms.CheckboxSelectMultiple(attrs={'class':'ul-no-bullets '}))
    # ref_codon = django_filters.MultipleChoiceFilter(choices=ref_codon_choices, widget=forms.CheckboxSelectMultiple(attrs={'class':'ul-no-bullets '}))
    # alt_codon = django_filters.MultipleChoiceFilter(choices=alt_codon_choices, widget=forms.CheckboxSelectMultiple(attrs={'class':'ul-no-bullets '}))
    # ref = django_filters.MultipleChoiceFilter(choices=ref_choices, widget=forms.CheckboxSelectMultiple(attrs={'class':'ul-no-bullets '}))
    # alt = django_filters.MultipleChoiceFilter(choices=alt_choices, widget=forms.CheckboxSelectMultiple(attrs={'class':'ul-no-bullets '}))


    class Meta:
        model = Sample
        fields = ['id_uvigo_id__id_uvigo', 'pos']