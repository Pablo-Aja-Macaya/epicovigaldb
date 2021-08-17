from django.contrib import admin

# Register your models here.
from .models import Status

class StatusAdmin(admin.ModelAdmin):
    search_fields = ['id_proceso, tarea']
    list_display = [f.name for f in Status._meta.fields]

admin.site.register(Status, StatusAdmin)