from django.db import models
from upload.models import Sample, Region
from upload.models import SampleMetaData
from tests.models import PicardTest, NextcladeTest, LineagesTest, NGSstatsTest, SingleCheckTest, VariantsTest
import django_tables2 as tables
import django_filters
from django_tables2.utils import A
# Create your models here.

# In[1]: Tablas de metadatos
class SampleTable(tables.Table):
    id_uvigo = tables.LinkColumn('specific_sample', args=[A('id_uvigo')])
    class Meta:
        model = Sample
        template_name = "table_template.html"

class RegionTable(tables.Table):
    id_uvigo = tables.LinkColumn('specific_sample', args=[A('id_uvigo')])
    class Meta:
        model = Region
        template_name = "table_template.html"

class SampleMetaDataTable(tables.Table):
    id_uvigo = tables.LinkColumn('specific_sample', args=[A('id_uvigo')])
    class Meta:
        model = SampleMetaData
        template_name = "table_template.html"

# In[2]: Tablas de resultados
class LineagesTable(tables.Table):
    id_uvigo = tables.LinkColumn('specific_sample', args=[A('id_uvigo')])
    class Meta:
        model = LineagesTest
        template_name = "table_template.html"

class PicardTable(tables.Table):
    id_uvigo = tables.LinkColumn('specific_sample', args=[A('id_uvigo')])
    class Meta:
        model = PicardTest
        template_name = "table_template.html"
        
class NextcladeTable(tables.Table):
    id_uvigo = tables.LinkColumn('specific_sample', args=[A('id_uvigo')])
    class Meta:
        model = NextcladeTest
        template_name = "table_template.html"

class NGSTable(tables.Table):
    id_uvigo = tables.LinkColumn('specific_sample', args=[A('id_uvigo')])
    class Meta:
        model = NGSstatsTest
        template_name = "table_template.html"

class VariantsTable(tables.Table):
    id_uvigo = tables.LinkColumn('specific_sample', args=[A('id_uvigo')])
    class Meta:
        model = VariantsTest
        template_name = "table_template.html"

class SingleCheckTable(tables.Table):
    id_uvigo = tables.LinkColumn('specific_sample', args=[A('id_uvigo')])
    class Meta:
        model = SingleCheckTest
        template_name = "table_template.html"


# In[3]: Tabla de tests completados
class CompletedTestsTable(tables.Table):
    # Tabla donde se indicará para cada muestra qué tests tiene hechos
    # 1 - Coger todos los nombres de Samples
    # 2 - Buscar estos nombres en las tablas de resultados, si aparecen poner un {sample:1},
    #     si no poner {sample:0}?
    # 3 - Renderizarlo en la tabla según si han sido testeadas (1) o no (0)
    # data = [
    #     {'sample':'epiblabla', 'picard':1, 'nextclade':0, 'ngsstats':1},
    #     {'sample':'epiblabla2', 'picard':1, 'nextclade':0, 'ngsstats':1},
    # ]

    id_uvigo = tables.LinkColumn('specific_sample', args=[A('id_uvigo')])
    picardtest = tables.Column(verbose_name='Picard')
    nextcladetest = tables.Column(verbose_name='NextClade')
    ngsstatstest = tables.Column(verbose_name='NGSStats')
    lineagestest = tables.Column(verbose_name='Pangolin')
    singlechecktest = tables.Column(verbose_name='SingleCheck')
    variantstest = tables.Column(verbose_name='iVar')
    class Meta:
        template_name = "table_template.html"


# In[4]: Filtros

class SampleFilter(django_filters.FilterSet):
    id_uvigo = django_filters.CharFilter(field_name = 'id_uvigo', lookup_expr='icontains')
    sexo = django_filters.CharFilter(field_name = 'sexo', lookup_expr='icontains')
    edad__gt = django_filters.NumberFilter(field_name = 'edad', lookup_expr='gt')
    edad__lt = django_filters.NumberFilter(field_name = 'edad', lookup_expr='lt')
    fecha_muestra = django_filters.DateFromToRangeFilter(field_name = 'fecha_muestra')

    class Meta:
        model = Sample
        fields = ['id_uvigo','sexo', 'edad', 'fecha_muestra']

class MetaDataFilter(django_filters.FilterSet):
    id_uvigo = django_filters.CharFilter(field_name = 'id_uvigo', lookup_expr='icontains')
    fecha_entrada_uv = django_filters.DateFromToRangeFilter(field_name = 'fecha_entrada_uv')

    class Meta:
        model = Sample
        fields = ['id_uvigo', 'fecha_entrada_uv']
                