# Generated by Django 3.1.3 on 2021-04-14 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0044_auto_20210414_0157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='samplemetadata',
            name='id_hospital',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='samplemetadata',
            name='id_muestra',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='samplemetadata',
            name='id_paciente',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='samplemetadata',
            name='numero_envio',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
