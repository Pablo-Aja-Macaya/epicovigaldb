# Generated by Django 3.1.3 on 2021-05-25 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0052_region_division'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='cp',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='region',
            name='division',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='region',
            name='latitud',
            field=models.TextField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='region',
            name='localizacion',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='region',
            name='longitud',
            field=models.TextField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='region',
            name='pais',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='region',
            name='region',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]
