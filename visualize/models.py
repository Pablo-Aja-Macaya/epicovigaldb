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
    id_uvigo = django_filters.CharFilter(field_name = 'id_uvigo', lookup_expr='icontains')
    categoria_muestra = django_filters.CharFilter(field_name = 'categoria_muestra', lookup_expr='icontains')
    nodo_secuenciacion = django_filters.CharFilter(field_name = 'nodo_secuenciacion', lookup_expr='icontains')
    fecha_muestra = django_filters.DateFromToRangeFilter(field_name = 'fecha_muestra')

    class Meta:
        model = Sample
        fields = ['id_uvigo','categoria_muestra','nodo_secuenciacion', 'fecha_muestra']

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

#
# class CompletedTestsFilter(django_filters.FilterSet):
#     id_uvigo = django_filters.CharFilter(field_name = 'id_uvigo', lookup_expr='icontains')
#     class Meta:
#         # model = Sample
#         fields = ['id_uvigo']

