from django.contrib import admin

from .models import Region, Sample, OurSampleCharacteristic


admin.site.register(Region)
admin.site.register(Sample)
admin.site.register(OurSampleCharacteristic)