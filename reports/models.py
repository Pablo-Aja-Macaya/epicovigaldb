from django.db import models
import datetime

# Create your models here.
class Report(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_inicial = models.DateField(blank=True, null=True)
    fecha_final = models.DateField(blank=True, null=True)
    variantes = models.TextField(max_length=50, default=None)
    subtitulo = models.TextField(max_length=50, default=None)
    texto = models.TextField(max_length=50, default=None, blank=True)

    def get_month(self):
        m = datetime.datetime.strptime(str(self.fecha_inicial), "%Y-%m-%d").strftime("%B")
        return m
    def get_year(self):
        y = datetime.datetime.strptime(str(self.fecha_inicial), "%Y-%m-%d").year
        return y
    def __str__(self):
        return f'{str(self.id)}'
