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
    variantstest__id_uvigo = tables.Column(verbose_name='iVar')
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
    fecha_entrada = django_filters.DateFromToRangeFilter(field_name = 'fecha_entrada')

    class Meta:
        model = SampleMetaData
        fields = ['id_uvigo', 'fecha_entrada']

# class CompletedTestsFilter(django_filters.FilterSet):
#     id_uvigo = django_filters.CharFilter(field_name = 'id_uvigo', lookup_expr='icontains')
#     class Meta:
#         # model = Sample
#         fields = ['id_uvigo']

# In[5]: Forms

class SampleForm(ModelForm):
    id_uvigo = forms.CharField(required=False, disabled=True)
    # cp = forms.IntegerField(required=False)
    # localizacion = forms.CharField(required=False)
    # categoria_muestra = forms.ChoiceField(choices=(('1','One'),("2", "Two")), required=False)
    id_region = forms.ModelChoiceField(queryset=Region.objects.all().order_by('localizacion'), required=False)#, disabled=True)
    class Meta:
        model = Sample
        fields = '__all__'
        exclude = ['data_path']#,'id_region']
        # widgets = {
        #     'id_uvigo': forms.TextInput(attrs={'disabled': True}),
        #     'id_region': forms.TextInput(attrs={'disabled': True}),
        # }

class SampleMetaDataForm(ModelForm):
    id_uvigo = forms.ModelChoiceField(queryset=Sample.objects.all() , required=False, disabled=True)
    class Meta:
        model = SampleMetaData
        fields = '__all__'
        exclude = ['data_path']

class RegionForm(ModelForm):
    id_region = forms.ModelChoiceField(queryset=Region.objects.all() , required=False, disabled=True)
    class Meta:
        model = Region
        fields = '__all__'

## Test forms
class SingleCheckForm(ModelForm):
    id_uvigo = forms.ModelChoiceField(queryset=Sample.objects.all() , required=False, disabled=True)
    class Meta:
        model = SingleCheckTest
        fields = '__all__'
class PicardForm(ModelForm):
    id_uvigo = forms.ModelChoiceField(queryset=Sample.objects.all() , required=False, disabled=True)
    class Meta:
        model = PicardTest
        fields = '__all__'
class NextcladeForm(ModelForm):
    id_uvigo = forms.ModelChoiceField(queryset=Sample.objects.all() , required=False, disabled=True)
    class Meta:
        model = NextcladeTest
        fields = '__all__'
class LineagesForm(ModelForm):
    id_uvigo = forms.ModelChoiceField(queryset=Sample.objects.all() , required=False, disabled=True)
    class Meta:
        model = LineagesTest
        fields = '__all__'
class NGSStatssForm(ModelForm):
    id_uvigo = forms.ModelChoiceField(queryset=Sample.objects.all() , required=False, disabled=True)
    class Meta:
        model = NGSstatsTest
        fields = '__all__'