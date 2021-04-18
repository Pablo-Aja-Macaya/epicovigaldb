# Generated by Django 3.1.3 on 2021-04-11 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0042_auto_20210411_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='samplemetadata',
            name='ct_gen_e',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='samplemetadata',
            name='ct_gen_n',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='samplemetadata',
            name='ct_orf1ab',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='samplemetadata',
            name='ct_redrp',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='samplemetadata',
            name='ct_s',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='samplemetadata',
            name='hospitalizacion',
            field=models.CharField(blank=True, default=None, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='samplemetadata',
            name='uci',
            field=models.CharField(blank=True, default=None, max_length=1, null=True),
        ),
    ]