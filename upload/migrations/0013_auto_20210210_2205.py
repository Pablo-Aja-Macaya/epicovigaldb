# Generated by Django 3.1.3 on 2021-02-10 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0012_oursamplecharacteristic_id_hospital'),
    ]

    operations = [
        migrations.AddField(
            model_name='oursamplecharacteristic',
            name='ct_s',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=5),
        ),
        migrations.AddField(
            model_name='oursamplecharacteristic',
            name='fecha_entrada_fastq_uvigo',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='oursamplecharacteristic',
            name='fecha_envio_cdna',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='oursamplecharacteristic',
            name='fecha_run_ngs',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='oursamplecharacteristic',
            name='ct_gen_e',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=5),
        ),
        migrations.AlterField(
            model_name='oursamplecharacteristic',
            name='ct_gen_n',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=5),
        ),
        migrations.AlterField(
            model_name='oursamplecharacteristic',
            name='ct_orf1ab',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=5),
        ),
        migrations.AlterField(
            model_name='oursamplecharacteristic',
            name='ct_redrp',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=5),
        ),
    ]
