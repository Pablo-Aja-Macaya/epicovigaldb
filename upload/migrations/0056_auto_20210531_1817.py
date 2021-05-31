# Generated by Django 3.1.3 on 2021-05-31 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0055_region_localizacion_org'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='vigilancia',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='samplemetadata',
            name='fecha_vacunacion_ultima_dosis',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
