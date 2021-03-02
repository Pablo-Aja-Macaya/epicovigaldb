from django.contrib import admin

from .models import Region, Sample, SampleMetaData

admin.site.register(Region)
admin.site.register(Sample)
admin.site.register(SampleMetaData)
