from django.db import models
from upload.models import Sample, Region, SampleMetaData
from tests.models import PicardTest, NextcladeTest, LineagesTest, NGSstatsTest, SingleCheckTest, VariantsTest
import django_tables2 as tables
# Create your models here.

# Tablas de metadatos
class SampleTable(tables.Table):
    class Meta:
        model = Sample
        template_name = "table_template.html"

class RegionTable(tables.Table):
    class Meta:
        model = Region
        template_name = "table_template.html"

class SampleMetaDataTable(tables.Table):
    class Meta:
        model = SampleMetaData
        template_name = "table_template.html"

# Tablas de resultados
class LineagesTable(tables.Table):
    class Meta:
        model = LineagesTest
        template_name = "table_template.html"

class PicardTable(tables.Table):
    class Meta:
        model = PicardTest
        template_name = "table_template.html"
        
class NextcladeTable(tables.Table):
    class Meta:
        model = NextcladeTest
        template_name = "table_template.html"

class NGSTable(tables.Table):
    class Meta:
        model = NGSstatsTest
        template_name = "table_template.html"

class VariantsTable(tables.Table):
    class Meta:
        model = VariantsTest
        template_name = "table_template.html"

class SingleCheckTable(tables.Table):
    class Meta:
        model = SingleCheckTest
        template_name = "table_template.html"

