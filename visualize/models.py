from django.db import models
from upload.models import Sample
import django_tables2 as tables
# Create your models here.


class SampleTable(tables.Table):
    class Meta:
        model = Sample
        template_name = "table_template.html"
