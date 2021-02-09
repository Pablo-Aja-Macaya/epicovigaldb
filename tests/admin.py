from django.contrib import admin

# Register your models here.
from .models import PicardTest, SingleCheckTest, NGSstatsTest, NextcladeTest, VariantsTest, LineagesTest

admin.site.register(PicardTest)
admin.site.register(SingleCheckTest)
admin.site.register(NGSstatsTest)
admin.site.register(NextcladeTest)
admin.site.register(VariantsTest)
admin.site.register(LineagesTest)