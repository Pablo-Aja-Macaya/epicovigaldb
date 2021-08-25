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
def get_choices(obj, campo):
    # Devuelve una tupla de tuplas con los distintos valores de un atributo para un objeto model determiando
    return [(i,i) for i in obj.values_list(campo,flat=True).distinct().order_by(campo).all() if i]

CHECKBOX_WIDGET = forms.CheckboxSelectMultiple(attrs={'class':'ul-no-bullets '})
TEXT_WIDGET = forms.widgets.TextInput(attrs={'class':'col-4 text-center form-control'})
RANGE_WIDGET = django_filters.widgets.RangeWidget(attrs={'class':'col-4 text-center form-control'})

class SampleFilter(django_filters.FilterSet):
    obj = Sample.objects.values('categoria_muestra','vigilancia','nodo_secuenciacion').distinct()
    choices_categoria = get_choices(obj, 'categoria_muestra')
    choices_vigilancia = get_choices(obj, 'vigilancia')
    choices_nodos = get_choices(obj, 'nodo_secuenciacion')
    choices_hospitales = get_choices(SampleMetaData.objects.values('id_hospital'), 'id_hospital')
    
    id_uvigo = django_filters.CharFilter(field_name = 'id_uvigo', lookup_expr='icontains', widget=TEXT_WIDGET)
    categoria_muestra = django_filters.MultipleChoiceFilter(choices=choices_categoria, widget=CHECKBOX_WIDGET)
    vigilancia = django_filters.MultipleChoiceFilter(choices=choices_vigilancia, widget=CHECKBOX_WIDGET)
    nodo_secuenciacion = django_filters.MultipleChoiceFilter(choices=choices_nodos, widget=CHECKBOX_WIDGET)
    fecha_muestra = django_filters.DateFromToRangeFilter(field_name = 'fecha_muestra', label='Fecha de muestra entre:', widget=django_filters.widgets.RangeWidget(attrs={'type': 'date', 'class':'col-4 text-center form-control'}))
    samplemetadata__id_hospital = django_filters.MultipleChoiceFilter(choices=choices_hospitales, label='Hospital', widget=CHECKBOX_WIDGET)
    class Meta:
        model = Sample
        fields = ['id_uvigo', 'fecha_muestra', 'samplemetadata__id_hospital', 'vigilancia', 'categoria_muestra', 'nodo_secuenciacion']

class MetaDataFilter(django_filters.FilterSet):
    id_uvigo = django_filters.CharFilter(field_name = 'id_uvigo', lookup_expr='icontains', widget=TEXT_WIDGET)
    fecha_entrada = django_filters.DateFromToRangeFilter(field_name = 'fecha_entrada', widget=django_filters.widgets.RangeWidget(attrs={'type': 'date', 'class':'col-4 text-center form-control'}))

    class Meta:
        model = SampleMetaData
        fields = ['id_uvigo', 'fecha_entrada']

class RegionFilter(django_filters.FilterSet):
    obj = Region.objects.values('localizacion','division','pais').distinct()
    choices_localizacion = get_choices(obj, 'localizacion')
    choices_division = get_choices(obj, 'division')
    choices_pais = get_choices(obj, 'pais')

    cp = django_filters.CharFilter(field_name = 'cp', lookup_expr='icontains', widget=TEXT_WIDGET)
    division = django_filters.MultipleChoiceFilter(choices=choices_division, widget=CHECKBOX_WIDGET)
    pais = django_filters.MultipleChoiceFilter(choices=choices_pais, widget=CHECKBOX_WIDGET)
    localizacion = django_filters.MultipleChoiceFilter(choices=choices_localizacion, widget=CHECKBOX_WIDGET)

    class Meta:
        model = Region
        fields = ['cp','division','pais','localizacion']


class NextcladeFilter(django_filters.FilterSet):
    clade_choices = get_choices(NextcladeTest.objects.values('clade'), 'clade')
    
    id_uvigo_id__id_uvigo = django_filters.CharFilter(field_name = 'id_uvigo_id__id_uvigo', lookup_expr='icontains', widget=TEXT_WIDGET)
    clade = django_filters.MultipleChoiceFilter(choices=clade_choices, widget=CHECKBOX_WIDGET)
    class Meta:
        model = Sample
        fields = ['id_uvigo_id__id_uvigo']

class PangolinFilter(django_filters.FilterSet):
    lineage_choices = get_choices(LineagesTest.objects.values('lineage'), 'lineage')
    
    id_uvigo_id__id_uvigo = django_filters.CharFilter(field_name = 'id_uvigo_id__id_uvigo', lookup_expr='icontains', widget=TEXT_WIDGET)
    lineage = django_filters.MultipleChoiceFilter(choices=lineage_choices, widget=CHECKBOX_WIDGET)
    class Meta:
        model = Sample
        fields = ['id_uvigo_id__id_uvigo']

class PicardFilter(django_filters.FilterSet):    
    id_uvigo_id__id_uvigo = django_filters.CharFilter(field_name = 'id_uvigo_id__id_uvigo', lookup_expr='icontains', widget=TEXT_WIDGET)
    mean_target_coverage = django_filters.RangeFilter(widget=RANGE_WIDGET)
    median_target_coverage = django_filters.RangeFilter(widget=RANGE_WIDGET)
    pct_target_bases_1x = django_filters.RangeFilter(widget=RANGE_WIDGET)
    pct_target_bases_10x = django_filters.RangeFilter(widget=RANGE_WIDGET)
    pct_target_bases_100x = django_filters.RangeFilter(widget=RANGE_WIDGET)
    class Meta:
        model = Sample
        fields = ['id_uvigo_id__id_uvigo']

class NGSFilter(django_filters.FilterSet):    
    id_uvigo_id__id_uvigo = django_filters.CharFilter(field_name = 'id_uvigo_id__id_uvigo', lookup_expr='icontains', widget=TEXT_WIDGET)
    total_reads = django_filters.RangeFilter(widget=RANGE_WIDGET)
    mapped = django_filters.RangeFilter(widget=RANGE_WIDGET)
    trimmed = django_filters.RangeFilter(widget=RANGE_WIDGET)
    class Meta:
        model = Sample
        fields = ['id_uvigo_id__id_uvigo']

class VariantsFilter(django_filters.FilterSet):
    obj = VariantsTest.objects.values('ref_aa','alt_aa')
    ref_aa_choices = get_choices(obj, 'ref_aa')
    alt_aa_choices = get_choices(obj, 'alt_aa')

    id_uvigo_id__id_uvigo = django_filters.CharFilter(label='id_uvigo', field_name = 'id_uvigo_id__id_uvigo', lookup_expr='icontains', widget=TEXT_WIDGET)
    pos = django_filters.RangeFilter(widget=RANGE_WIDGET)
    ref_aa = django_filters.MultipleChoiceFilter(choices=ref_aa_choices, widget=CHECKBOX_WIDGET)
    alt_aa = django_filters.MultipleChoiceFilter(choices=alt_aa_choices, widget=CHECKBOX_WIDGET)


    class Meta:
        model = Sample
        fields = ['id_uvigo_id__id_uvigo', 'pos']