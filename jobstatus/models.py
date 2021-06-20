from django.db import models
import django_tables2 as tables
import django_filters
from django_tables2.utils import A

# Create your models here.
class Status(models.Model):
    status_choices = [
        ('O', 'En curso'),
        ('C', 'Completado'),
        ('S', 'Almacenado'),
        ('F', 'Fallido'),
    ]
    id_proceso = models.CharField(max_length=40, primary_key=True)
    tarea = models.TextField(max_length=50)
    status = models.CharField(max_length=20, choices=status_choices)
    comentario = models.TextField(max_length=500)
    fecha = models.DateTimeField()
    tiempo = models.IntegerField()

    def __str__(self):
        return str(self.tarea)


############
# Tablas
class StatusTable(tables.Table):
    fecha = tables.DateTimeColumn(format ='d/m/Y, h:i A')
    class Meta:
        model = Status
        template_name = "table_template.html"