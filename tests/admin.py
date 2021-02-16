from django.contrib import admin

# Register your models here.
from .models import SingleCheckTest, NGSstatsTest, NextcladeTest
from .models import PicardTest, LineagesTest, LineagesMostCommonCountries
from .models import VariantsTest

admin.site.register(PicardTest)
admin.site.register(SingleCheckTest)
admin.site.register(NGSstatsTest)
admin.site.register(NextcladeTest)
admin.site.register(VariantsTest)
admin.site.register(LineagesTest)
admin.site.register(LineagesMostCommonCountries)